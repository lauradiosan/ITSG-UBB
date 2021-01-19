"""
Detectron MaskRCNN pe object detection
"""
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
import cv2
from detectron2.data import DatasetCatalog, MetadataCatalog

from Models.Detectron2.detectron2.detectron2.engine import DefaultTrainer
from detectron2 import model_zoo
import os
from PIL import Image
from Utils.ImageUtils import ImageUtils
from detectron2.data.datasets import register_coco_instances
from Utils.MaskUtils import MaskUtils
from Utils.FileUtils import FileUtils
from Utils.CocoUtils import CocoUtils


class DetectronBladder:
    def __init__(self):
        self.image_utils = ImageUtils()
        self.mask_utils = MaskUtils()
        self.file_utils = FileUtils()
        self.coco_utils = CocoUtils()

        self.cfg = None
        self.predictor = None
        self.bladder_metadata = None

        self.configure()

    def configure(self):
        self.cfg = get_cfg()
        self.cfg.OUTPUT_DIR = "./Output/Bladder"
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
        self.cfg.MODEL.WEIGHTS = os.path.join(self.cfg.OUTPUT_DIR, "model_final.pth")
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        self.predictor = DefaultPredictor(self.cfg)
        self.bladder_metadata = MetadataCatalog.get("bladder_test")

    def train(self):
        os.makedirs(self.cfg.OUTPUT_DIR, exist_ok=True)
        trainer = DefaultTrainer(self.cfg)
        trainer.resume_or_load(resume=False)
        trainer.train()

    def register_dataset(self):
        for d in ["train", "test"]:
            register_coco_instances(f"bladder_{d}", {}, f"Data/Vezica/{d}.json", f"Data/Vezica/{d}")

    def process_result(self, image_path, outputs, output):
        try:
            instances = outputs["instances"].to("cpu")
            if instances.has("pred_boxes") and len(instances.pred_boxes) > 0:
                if output != "":
                    im2 = Image.open(image_path)
                    img = self.image_utils.get_masked_image(im2, instances.pred_masks[0])
                    img.save(output)
                return True, instances.pred_masks[:1], ""
            else:
                return False, [], ""
        except Exception as e:
            return False, [], str(e)

    def test_detect(self, images_folder, output_folder, test_files, width, height):
        ious = []
        dscs = []
        for (image_path, json_path) in test_files:
            output_path = output_folder + image_path
            is_bladder, pred_masks, err = self.detect_bladder(images_folder + image_path, output_path)

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

    def detect_bladder(self, image_path, output_path):
        im = cv2.imread(image_path)

        outputs = self.predictor(im)

        return self.process_result(image_path, outputs, output_path)
