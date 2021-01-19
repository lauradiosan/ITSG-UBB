"""
Detectron MaskRCNN pe object detection
"""
from detectron2.structures import Instances
from detectron2.utils.visualizer import Visualizer
import cv2
from detectron2.utils.visualizer import ColorMode
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import nrrd
from Utils.ImageUtils import ImageUtils
from shutil import copyfile
import base64
from Models.Detectron2.DetectronBladder import DetectronBladder
from Models.Detectron2.DetectronBladderTumor import DetectronBladderTumor
from Utils.FileUtils import FileUtils


class DetectronWrapper():
    def __init__(self):
        self.image_utils = ImageUtils()
        self.file_utils = FileUtils()

        self.detectron_bladder = DetectronBladder()
        self.detectron_tumor = DetectronBladderTumor()

    def create_result_folders(self, userID, imageDate):
        user_folder = self.file_utils.create_folder("./Data/Server/" + str(userID) + "/")

        out = self.file_utils.create_folder(user_folder + imageDate + "/")

        return out

    def save_image(self, bytes, path, skipped):
        npbytes = base64.b64decode(bytes[skipped:])
        file = open(path, "wb")
        file.write(npbytes)
        file.close()
        return path

    def save_png_images(self, output_folder, readdata):
        k = 1

        png_images = []
        png_image_paths = []

        for x in readdata[:][:]:
            file_path = str(k) + ".png"
            plt.imsave(output_folder + file_path, x, cmap="gray")
            png_images.append(k)
            png_image_paths.append(file_path)
            k += 1

        return png_images, png_image_paths

    def obtain_png_images(self, output_folder, imageName, imageBytes):
        path = self.save_image(imageBytes, output_folder + imageName, 37)

        readdata, header = nrrd.read(path, index_order='C')

        return self.save_png_images(output_folder, readdata)

    def detect_bladder(self, png_images, output_folder):
        bladder_out = self.file_utils.create_folder(output_folder + "Bladder/")

        bladder_images = []
        bladder_masks = []

        for p in png_images:
            file_path = output_folder + str(p) + ".png"
            out_path = bladder_out + str(p) + ".png"
            found, mask, err = self.detectron_bladder.detect_bladder(file_path, out_path)
            if found:
                bladder_images.append(p)
                bladder_masks.append(mask)

        bladder_image_paths, bladder_masks = self.image_utils.get_longest_sequence_paths(bladder_images, bladder_masks)

        return bladder_image_paths, bladder_masks, bladder_out

    def detect_tumor(self, bladder_image_paths, bladder_folder):
        # tumor_out = self.file_utils.create_folder(output_folder + "Tumor/")

        tumor_images = []
        tumor_masks = []

        print("Tumor")

        for p in bladder_image_paths:
            file_path = bladder_folder + str(p)
            print(file_path)
            # out_path = tumor_out + str(p)
            mask, err = self.detectron_tumor.detect_tumor(file_path)#, out_path)
            if mask != []:
                tumor_images.append(p)
                tumor_masks.append(mask)

        # tumor_images, tumor_masks = self.image_utils.get_longest_sequence_paths(tumor_images, tumor_masks)

        return tumor_images, tumor_masks

    def get_bladder_tumor_indices(self, bladder_image_paths, tumor_images, name):
        bladder_i = -1
        tumor_i = -1
        try:
            bladder_i = bladder_image_paths.index(name)
            tumor_i = tumor_images.index(name)
        except:
            pass

        return bladder_i, tumor_i

    def save_output_image(self, im, masks, output_path, input_path):
        instances = Instances((512, 512))
        instances.pred_masks = masks

        if len(instances.pred_masks) > 0:
            v = Visualizer(np.flip(im[:, :, ::-1], 1),
                           metadata=self.detectron_tumor.tumor_metadata,
                           scale=0.8,
                           instance_mode=ColorMode.IMAGE_BW  # remove the colors of unsegmented pixels
                           )
            v = v.draw_instance_predictions(instances)
            plt.figure(figsize=(14, 10))
            img = np.flip(v.get_image()[:, :, ::-1], 1)
            img = Image.fromarray(img, 'RGB')
            img.save(output_path)
        else:
            copyfile(input_path, output_path)

    def get_output_image_path(self, final_output, output_folder, png_path, bladder_image_paths,
                              tumor_images, tumor_masks):
        output_path = final_output + png_path
        input_path = output_folder + png_path
        im = cv2.imread(input_path)

        bladder_i, tumor_i = self.get_bladder_tumor_indices(bladder_image_paths, tumor_images, str(png_path))

        if bladder_i != -1 and tumor_i != -1 and len(tumor_masks[tumor_i]) > 0:
            self.save_output_image(im, tumor_masks[tumor_i], output_path, input_path)
        else:
            copyfile(input_path, output_path)

        return output_path

    def get_output_bytes(self, output_folder, png_image_paths, bladder_image_paths, tumor_images, tumor_masks):
        final_output = self.file_utils.create_folder(output_folder + "Output/")

        resultBytes = []

        for i in range(len(png_image_paths)):
            output_path = self.get_output_image_path(final_output, output_folder, png_image_paths[i],
                                                     bladder_image_paths, tumor_images, tumor_masks)

            resultBytes.append(self.image_utils.image_to_bytes(output_path))

        return resultBytes

    def clean_up(self, userID, bladder_folder, output_folder):
        if userID == "guest":
            self.file_utils.delete_folder(output_folder)
        else:
            self.file_utils.delete_folder(bladder_folder)
            self.file_utils.delete_files(output_folder, ".png")
            self.file_utils.delete_files(output_folder, ".nrrd")

    def obtain_png_from_png(self, output_folder, imageBytes):
        png_images = [1]
        png_image_paths = ["1.png"]

        self.save_image(imageBytes, output_folder + "1.png", 22)

        return png_images, png_image_paths

    def detect_file(self, userID, imageDate, imageName, imageBytes):
        output_folder = self.create_result_folders(userID, imageDate)

        if self.file_utils.is_of_type(imageName, ".nrrd"):
            png_images, png_image_paths = self.obtain_png_images(output_folder, imageName, imageBytes)
        else:
            png_images, png_image_paths = self.obtain_png_from_png(output_folder, imageBytes)

        print(png_image_paths)
        print(png_images)

        bladder_image_paths, bladder_masks, bladder_folder = self.detect_bladder(png_images, output_folder)

        print(bladder_image_paths)

        tumor_images, tumor_masks = self.detect_tumor(bladder_image_paths, bladder_folder)

        resultBytes = self.get_output_bytes(output_folder, png_image_paths, bladder_image_paths,
                                            tumor_images, tumor_masks)

        self.clean_up(userID, bladder_folder, output_folder)

        return resultBytes

    def get_record_images(self, userID, imageDate):
        user_folder = "Data/Server/" + userID + "/"
        if not self.file_utils.file_exists(user_folder):
            return []

        record_folder = user_folder + imageDate + "/"
        if not self.file_utils.file_exists(record_folder):
            return []

        images_folder = record_folder + "Output/"
        if not self.file_utils.file_exists(images_folder):
            return []

        resultBytes = []
        for file in self.file_utils.get_files_in_folder(images_folder):
            file_path = images_folder + file
            resultBytes.append(self.image_utils.image_to_bytes(file_path))

        return resultBytes
