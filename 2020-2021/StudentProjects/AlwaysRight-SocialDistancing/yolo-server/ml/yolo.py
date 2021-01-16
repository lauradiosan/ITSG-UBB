from typing import List, Tuple

import numpy as np
from PIL import Image
import pydarknet
import os
import numpy


class Prediction(object):
    def __init__(self, center: Tuple[int, int], bounding_box: Tuple[int, int, int, int], prediction_id: int):
        self.center = center
        self.bounding_box = bounding_box
        self.pid = prediction_id

    def __eq__(self, other):
        if not isinstance(other, Prediction):
            return False

        return self.pid == other.pid

    def __str__(self):
        return 'id: {0} center: {1} bounding box: {2}'.format(self.pid, self.center, self.bounding_box)


class Yolo(object):
    def __init__(self, weights_path: str, config_path: str, labels_path: str, **kwargs):
        self._model = self._initialize(weights_path, config_path, labels_path)

        self._PERSON_LABEL = b'person\r'
        self.confidence_threshold = 0.6

        if 'confidence_threshold' in kwargs:
            self.confidence_threshold = kwargs['confidence_threshold']

    @staticmethod
    def _initialize(weights_path: str, config_path: str, labels_path: str):
        """
        Initializes the yolo model with the provided weights and config.
        :param weights_path: The nn weights.
        :param config_path: The yolo arhitecture config.
        :param labels_path: The path to the coco labels data.
        :return: the yolo model.
        """
        model = pydarknet.Detector(bytes(config_path, encoding="utf-8"), bytes(weights_path,
                                                                               encoding="utf-8"), 0, bytes(labels_path, encoding="utf-8"))
        return model

    def _get_prediction_from_detection(self, x: int, y: int, width: int, height: int, prediction_id: int) -> Prediction:
        """
            Return the bounding boxes for the current detection in terms of (x1, y1) and (x2, y2) where x1 and y1 are the leftmost points.
        """
        x1, y1, x2, y2 = int(x - width / 2), int(y - height /
                                                 2), int(x + width / 2), int(y + height / 2)
        return Prediction((x, y), (x1, y1, x2, y2), prediction_id)

    def _is_person_label(self, label):
        """
        Check wether the current label represents a person detection.
        :param label: the detection label
        :return: true if the label represent a person detection, false otherwise
        """
        return self._PERSON_LABEL == label

    def _get_predictions_from_detections(self, detections) -> List[Prediction]:
        """
        Get the bounding boxes for the person detections.
        :param detections: the person detections from the model
        :return: the bounding boxes for the detections
        """
        matching_detections = filter(lambda x: self._is_person_label(
            x[0]) and x[1] >= self.confidence_threshold, detections)

        predictions = []
        for i, detection in enumerate(matching_detections):
            predictions.append(
                self._get_prediction_from_detection(*detection[2], i))
        return predictions

    def predict(self, image: Image) -> List[Prediction]:
        """
        Predict bounding boxes for the persons in the image.
        :param image: the PIL image
        :return: the bounding boxes for the persons in the image.
        """
        img = numpy.asarray(image)
        img_darknet = pydarknet.Image(img)

        detections = self._model.detect(img_darknet)
        predictions = self._get_predictions_from_detections(detections)
        return list(predictions)
