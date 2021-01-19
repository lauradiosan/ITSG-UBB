"""
Detectron MaskRCNN pe object detection
"""
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
import cv2
from detectron2.data import DatasetCatalog, MetadataCatalog

from Models.Detectron2.detectron2.detectron2.engine import DefaultTrainer
from detectron2 import model_zoo
import os
from detectron2.utils.visualizer import ColorMode
import matplotlib.pyplot as plt
from Utils.ImageUtils import ImageUtils
from Utils.MaskUtils import MaskUtils
from Utils.FileUtils import FileUtils
from Utils.CocoUtils import CocoUtils


class DetectronBladderTumor:
    def __init__(self):
        self.image_utils = ImageUtils()
        self.mask_utils = MaskUtils()
        self.file_utils = FileUtils()
        self.coco_utils = CocoUtils()

        self.cfg = None
        self.predictor = None
        self.tumor_metadata = None

        self.configure()

    def configure(self):
        self.cfg = get_cfg()
        self.cfg.OUTPUT_DIR = "./Output/Tumor"
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
        self.cfg.MODEL.WEIGHTS = os.path.join(self.cfg.OUTPUT_DIR, "model_final.pth")
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        self.predictor = DefaultPredictor(self.cfg)
        self.tumor_metadata = MetadataCatalog.get("tumor_test")

    def train(self):
        os.makedirs(self.cfg.OUTPUT_DIR, exist_ok=True)
        trainer = DefaultTrainer(self.cfg)
        trainer.resume_or_load(resume=False)
        trainer.train()

    def save_resulted_image(self, im, instances, output_path):
        v = Visualizer(im[:, :, ::-1],
                       metadata=self.tumor_metadata,
                       scale=0.8,
                       instance_mode=ColorMode.IMAGE_BW
                       )
        v = v.draw_instance_predictions(instances)
        plt.figure(figsize=(14, 10))
        img = v.get_image()[:, :, ::-1]

        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if output_path != "":
            resized = cv2.resize(img, (512, 512), interpolation=cv2.INTER_AREA)
            cv2.imwrite(output_path, resized)

        plt.close()

    def process_result(self, outputs):
        instances = outputs["instances"].to("cpu")

        # self.save_resulted_image(im, instances, output_path)

        if instances.has("pred_masks") and len(instances.pred_masks) > 0:
            return instances.pred_masks, ""
        else:
            return [], ""

    def detect_tumor(self, image_path):
        im = cv2.imread(image_path)

        outputs = self.predictor(im)

        return self.process_result(outputs)

    def test_detect(self, images_folder, output_folder, test_files, width, height):
        ious = []
        dscs = []
        for (image_path, json_path) in test_files:
            output_path = output_folder + image_path
            pred_masks, err = self.detect_tumor(images_folder + image_path)

            if json_path is not None:
                masks = self.coco_utils.json_annotation_to_masks(images_folder + json_path)
            else:
                masks = None
            output_mask = self.mask_utils.combine_masks(pred_masks, width, height)
            self.mask_utils.draw_mask(output_mask, output_path[:-4] + "-m.png")
            expected_mask = self.mask_utils.combine_masks(masks, width, height)
            self.mask_utils.draw_mask(expected_mask, output_path[:-4] + "-m2.png")

            intersection, union, sum = self.mask_utils.get_intersection_union_sum(expected_mask, output_mask)

            if union == 0:
                if intersection == 0:
                    iou = 1
                else:
                    iou = 0
            else:
                iou = intersection/union

            if iou <= 0.1:
                print(image_path)

            if sum == 0:
                dsc = 1
            else:
                dsc = (2 * intersection) / sum

            ious.append(iou)
            dscs.append(dsc)

        return ious, dscs

    def get_IOU_DSC(self, images_folder, output_folder):
        test_files = self.file_utils.get_test_files(images_folder)
        ious, dscs = self.test_detect(images_folder, output_folder, test_files, 512, 512)
        return sum(ious) / len(ious), sum(dscs) / len(dscs)
