"""
Load .mdh file as 3D numpy array
"""
# import SimpleITK as sitk
import numpy as np
# import matplotlib.pyplot as plt
import PIL.Image as Image
import io
from base64 import encodebytes, b64decode
import os
import png
import pydicom as dicom
import argparse

from PIL import ImageOps


class ImageUtils:
    def __init__(self):
        pass

    #
    # def load_itk(self, filename):
    #     # Reads the image using SimpleITK
    #     itkimage = sitk.ReadImage(filename)
    #
    #     # Convert the image to a  numpy array first and then shuffle the dimensions to get axis in the order z,y,x
    #     ct_scan = sitk.GetArrayFromImage(itkimage)
    #
    #     # Read the origin of the ct_scan, will be used to convert the coordinates from world to voxel and vice versa.
    #     origin = np.array(list(reversed(itkimage.GetOrigin())))
    #
    #     # Read the spacing along each dimension
    #     spacing = np.array(list(reversed(itkimage.GetSpacing())))
    #
    #     return ct_scan, origin, spacing
    #
    # """
    # Plot all segmentations from a .mhd image
    # """
    #
    # def plot_mhd(self, file):
    #     ct_scans = sitk.GetArrayFromImage(sitk.ReadImage(file, sitk.sitkFloat32))
    #     plt.figure(figsize=(20, 16))
    #     plt.gray()
    #     plt.subplots_adjust(0, 0, 1, 1, 0.01, 0.01)
    #     for i in range(ct_scans.shape[0]):
    #         plt.subplot(5, 6, i + 1), plt.imshow(ct_scans[i]), plt.axis('off')
    #     plt.show()
    #
    def get_longest_sequence_paths(self, values, masks):
        if values is None:
            return [], []

        if len(values) <= 1:
            return [str(x) + ".png" for x in values], masks

        currentPosition = 0
        currentLongestRun = 0
        startOfLongestRun = 0

        while currentPosition < len(values) - 3:
            startOfRun = currentPosition
            while (currentPosition < len(values) - 1 and values[currentPosition] + 1 == values[currentPosition + 1]) or \
                    (currentPosition < len(values) - 2 and values[currentPosition] + 2 == values[currentPosition + 2]):
                currentPosition += 1

            if currentPosition - startOfRun > currentLongestRun:
                startOfLongestRun = startOfRun
                currentLongestRun = currentPosition - startOfRun

            currentPosition += 1

        result = []
        result_masks = []

        for i in range(startOfLongestRun, startOfLongestRun + currentLongestRun + 1):
            result.append(str(values[i]) + ".png")
            result_masks.append(masks[i])

        return result, result_masks

    def image_to_bytes(self, path):
        # with open(path, "rb") as f:
        #     result = bytearray(f.read())
        #     return result
        # pil_img = Image.open(path, mode='r')  # reads the PIL image
        # byte_arr = io.BytesIO()
        # pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
        # encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64
        # return encoded_img

        pilImg = Image.open(path, mode='r')  # reads the PIL image
        bytearr = io.BytesIO()
        pilImg.save(bytearr, format='PNG')  # convert the PIL image to byte array
        encodedImg = encodebytes(bytearr.getvalue()).decode('ascii')  # encode as base64
        return encodedImg

    def bytes_to_image(self, bytearr, path):
        imgdata = b64decode(bytearr)
        with open(path, 'wb') as f:
            f.write(imgdata)

    def mri_to_png(self, mri_file, png_file):
        """ Function to convert from a DICOM image to png
            @param mri_file: An opened file like object to read te dicom data
            @param png_file: An opened file like object to write the png data
        """
        # Extracting data from the mri file
        plan = dicom.read_file(mri_file)
        shape = plan.pixel_array.shape

        image_2d = []
        max_val = 0
        for row in plan.pixel_array:
            pixels = []
            for col in row:
                pixels.append(col)
                if col > max_val: max_val = col
            image_2d.append(pixels)

        # Rescaling grey scale between 0-255
        image_2d_scaled = []
        for row in image_2d:
            row_scaled = []
            for col in row:
                col_scaled = int((float(col) / float(max_val)) * 255.0)
                row_scaled.append(col_scaled)
            image_2d_scaled.append(row_scaled)

        # Writing the PNG file
        w = png.Writer(shape[1], shape[0], greyscale=True)
        w.write(png_file, image_2d_scaled)

    def convert_file(self, mri_file_path, png_file_path):
        """ Function to convert an MRI binary file to a
            PNG image file.
            @param mri_file_path: Full path to the mri file
            @param png_file_path: Fill path to the png file
        """

        # Making sure that the mri file exists
        if not os.path.exists(mri_file_path):
            raise Exception('File "%s" does not exists' % mri_file_path)

        # Making sure the png file does not exist
        if os.path.exists(png_file_path):
            raise Exception('File "%s" already exists' % png_file_path)

        mri_file = open(mri_file_path, 'rb')
        png_file = open(png_file_path, 'wb')

        self.mri_to_png(mri_file, png_file)

        png_file.close()

    def convert_folder(self, mri_folder, png_folder):
        """ Convert all MRI files in a folder to png files
            in a destination folder
        """

        # Create the folder for the pnd directory structure
        os.makedirs(png_folder)

        # Recursively traverse all sub-folders in the path
        for mri_sub_folder, subdirs, files in os.walk(mri_folder):
            for mri_file in os.listdir(mri_sub_folder):
                mri_file_path = os.path.join(mri_sub_folder, mri_file)

                # Make sure path is an actual file
                if os.path.isfile(mri_file_path):

                    # Replicate the original file structure
                    rel_path = os.path.relpath(mri_sub_folder, mri_folder)
                    png_folder_path = os.path.join(png_folder, rel_path)
                    if not os.path.exists(png_folder_path):
                        os.makedirs(png_folder_path)
                    png_file_path = os.path.join(png_folder_path, '%s.png' % mri_file)

                    try:
                        # Convert the actual file
                        self.convert_file(mri_file_path, png_file_path)
                    except Exception as e:
                        print('FAIL>', mri_file_path, '-->', png_file_path, ':', e)

    def change_color_in_folder(self, folder, old_color, new_color):
        for file in os.listdir(folder):
            picture = Image.open(folder + file)

            width, height = picture.size

            for x in range(width):
                for y in range(height):
                    current_color = picture.getpixel((x, y))
                    if current_color == old_color:
                        picture.putpixel((x, y), new_color)
            picture.save(folder + file)

    def image_to_pixels(self, path):
        picture = Image.open(path)
        # picture = picture.convert('L')

        pixels = []

        width, height = picture.size

        for x in range(width):
            pixels.append([])
            for y in range(height):
                pixels[x].append(picture.getpixel((x, y)))
            pixels[x] = np.array(pixels[x])

        return pixels

    def get_masked_image(self, image, mask):
        image = ImageOps.mirror(image)
        image = image.rotate(90)
        width, height = image.size

        for x in range(width):
            for y in range(height):
                if not mask[x][y]:
                    image.putpixel((x, y), 0)

        return image.rotate(-90)

    def get_images(self):
        folder = "Data/Vezica/BladderResults/"
        resultBytes = []
        for file in os.listdir(folder):
            file_path = folder + file
            resultBytes.append(self.image_to_bytes(file_path))
        return resultBytes

    def get_record_images(self, userID, imageDate):
        user_folder = "Data/Server/" + userID + "/"
        if not os.path.exists(user_folder):
            return []

        record_folder = user_folder + imageDate + "/"
        if not os.path.exists(record_folder):
            return []

        images_folder = record_folder + "Output/"
        if not os.path.exists(images_folder):
            return []

        resultBytes = []
        for file in os.listdir(images_folder):
            file_path = images_folder + file
            resultBytes.append(self.image_to_bytes(file_path))
        return resultBytes
