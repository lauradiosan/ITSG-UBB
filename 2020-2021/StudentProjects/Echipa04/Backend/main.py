"""
Detect object masks using Detectron2
"""
# from Models.Detectron2.DetectronUtils import Detectron
# detectron = Detectron()
# detectron.detect_masks("Data/grane.jpg", "doodle_out.jpg", 3)


"""
Read NRRD files
"""
# import numpy as np
# import nrrd
# import matplotlib.pyplot as plt
# import os
#
# path = "Data/Vezica_1/"
# out = "Data/Vezica_1_Out/"
#
# for file in os.listdir(path):
#     file_path = path + file
#
#     readdata, header = nrrd.read(file_path, index_order='C')
#
#     k = 1
#
#     for x in readdata[:][:]:
#         strk = str(k)
#         if len(strk) == 1:
#             strk = '0' + strk
#         plt.imsave(out + strk + ".jpg", x)
#         k+=1




"""
Plot DICOM ?
"""
# from pydicom import dcmread, read_file
# from PIL.Image import fromarray
import os
# from skimage import exposure
# from pydicom.pixel_data_handlers.util import apply_voi_lut
# import matplotlib.pyplot as plt
# import cv2
# import SimpleITK as sitk
# from Utils.ImageUtils import convert_folder
#
# folder = "Data/Prostata/DX_DICOM/"
# out = "Data/Prostata/DX_PNG_2/"
#
# for file in os.listdir(folder):
#     os.rename(folder+file, folder + "82" + file[1:])
#
# convert_folder(folder, out)

# folder = "Data/Prostata/DX_PNG/"
#
# for file in os.listdir(folder):
#     # print(folder + file[:-8] + file[-4:])
#     os.rename(folder+file, folder + file[:-8] + file[-4:])

# i = "ProstateDx-01-0001_"
# k = 1
# for file in os.listdir(folder):
#     # out_folder = out + i
#     # if not os.path.exists(out_folder):
#     #     os.mkdir(out_folder)
#
#     # df_t = dcmread(folder + file)
#     # plt.imshow(df_t.pixel_array, cmap='gray')
#     # plt.axis('off')
#     # plt.savefig(out + i + str(k) + ".png", bbox_inches='tight')
#     # k += 1
#     # plt.close()
#
#     img = sitk.ReadImage(folder + file)
#     # rescale intensity range from [-1000,1000] to [0,255]
#     img = sitk.IntensityWindowing(img, -10000, 10000, 0, 255)
#     # convert 16-bit pixels to 8-bit
#     img = sitk.Cast(img, sitk.sitkUInt8)
#
#     sitk.WriteImage(img, out + i + str(k) + ".png")
#
#     k+=1
#     # for df in df_t.pixel_array:
#     #     plt.imshow(df, cmap='gray')
#     #     plt.axis('off')
#     #     plt.savefig(out_folder + "/" + str(k) + ".png", bbox_inches='tight')
#     #     k+=1
#     #     plt.close()


"""
Save one segmentation as png
"""
# from Utils.ImageUtils import load_itk
# import matplotlib.pyplot as plt
# s1, s2, s3 = load_itk("Data/ProstateX-0001-Ktrans.mhd")
# k = 1
# for x in s1:
#     plt.imsave("Trying/" + str(k) + ".png", x)
#     k+=1
#

"""
Convert PNG files in folder to COCO json format
"""
# from Utils.CocoUtils import pngToCoco
#
# pngToCoco("Data/Prostata/DX_Segmentations/test_old/")



"""
Convert raw to png
"""
# from PIL import Image
# rawData = open("Case01_segmentation.raw", 'rb').read()
# imgSize = (512, 512)# the image size
# img = Image.frombytes('L', imgSize, rawData)
# img.save("foo.jpg")# can give any format you like .png



from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
import os
import detectron2
from detectron2.utils.logger import setup_logger

# import some common libraries
import numpy as np
import cv2
import matplotlib.pyplot as plt

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import random
from detectron2.data import DatasetCatalog, MetadataCatalog


def train_detectron():
    setup_logger()

    """
    Register dataset
    """
    from detectron2.data.datasets import register_coco_instances

    for d in ["train", "test"]:
        register_coco_instances(f"bladder_masked_{d}", {}, f"Data/Vezica/Tumor_Masked/{d}.json",
                                f"Data/Vezica/Tumor_Masked/{d}")


    """
    Display 3 random images from the dataset
    """
    import random
    from detectron2.data import DatasetCatalog, MetadataCatalog

    dataset_dicts = DatasetCatalog.get("bladder_masked_train")
    bladder_masked_metadata = MetadataCatalog.get("bladder_masked_train")

    # for d in random.sample(dataset_dicts, 1):
    #     img = cv2.imread(d["file_name"])
    #     v = Visualizer(img[:, :, ::-1], metadata=bladder_masked_metadata, scale=0.5)
    #     v = v.draw_dataset_dict(d)
    #     plt.figure(figsize = (14, 10))
    #     plt.imshow(cv2.cvtColor(v.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
    #     plt.show()


    """
    Train
    """

    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.DATASETS.TRAIN = ("bladder_masked_train",)
    cfg.DATASETS.TEST = ()
    cfg.DATALOADER.NUM_WORKERS = 1
    cfg.OUTPUT_DIR = "./Output/Bladder_Masked"
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
    # cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.SOLVER.IMS_PER_BATCH = 1
    cfg.SOLVER.BASE_LR = 0.00025
    cfg.SOLVER.MAX_ITER = 1500
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1

    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    trainer = DefaultTrainer(cfg)
    # trainer.resume_or_load(resume=False)
    trainer.train()

    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    cfg.DATASETS.TEST = ("bladder_masked_test",)
    predictor = DefaultPredictor(cfg)

    from detectron2.utils.visualizer import ColorMode
    from detectron2.evaluation.sem_seg_evaluation import SemSegEvaluator

    dataset_dicts = DatasetCatalog.get("bladder_masked_test")
    bladder_masked_metadata = MetadataCatalog.get("bladder_masked_test")

    # evaluator = SemSegEvaluator("bladder_masked_test", False, 2)
    # evaluator.evaluate()

    k = 1

    for d in dataset_dicts:
        im = cv2.imread(d["file_name"])
        outputs = predictor(im)
        v = Visualizer(im[:, :, ::-1],
                       metadata=bladder_masked_metadata,
                       scale=0.8,
                       instance_mode=ColorMode.IMAGE_BW  # remove the colors of unsegmented pixels
                       )
        v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        plt.figure(figsize=(14, 10))
        plt.imsave("test" + str(k) + ".png", cv2.cvtColor(v.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
        k+=1


# import torch
#
# def run():
#     torch.multiprocessing.freeze_support()
#     print('loop')
#     train_detectron()
#
# if __name__ == '__main__':
#     run()

"""
Save bladder cropped files
"""
# from Models.Detectron2.DetectronUtils import Detectron
# import os
#
# det = Detectron()
#
# folder = "Data/Vezica/PNG"
# out = "Data/Vezica/Cropped/"
#
# for file in os.listdir(folder):
#     if ".png" in file:
#         file_path = folder + "/" + file
#         det.detect_bladder(file_path, False, False, True, out + file)


"""
Run detectron for all images
"""
#
# from Models.Detectron2.DetectronWrapper import DetectronWrapper
# import os
# import base64
#
# det = DetectronWrapper()
#
# file = "Data/Vezica/Nrrd/cocan.nrrd"
#
# data_file = open("file.txt", "r")
# npbytes = base64.b64decode(data_file.read())
# # f = open("nrrrrrrd.nrrd", "wb")
# # f.write(npbytes)
# # f.close()
#
# print(det.detect_nrrd("9faadc3d-0f5e-4311-87d5-2072f8a3c545", "2021-01-12 17-05", "cocan.nrrd", npbytes))

from Models.Detectron2.DetectronWrapper import DetectronWrapper

detectron = DetectronWrapper()
# print(detectron.get_average_bladder_iou("Data/Vezica/Organ/test/", "Data/Vezica/TestResults/Organ/"))
#
# print(detectron.get_IOU_DSC("Data/Vezica/Tumor_Masked/test/", "Data/Vezica/Test_New_Conf/"))

file = open("file.txt", "r")
imageBytes = file.read()
file.close()

detectron.detect_file("1", "123", "1.nrrd", imageBytes)
