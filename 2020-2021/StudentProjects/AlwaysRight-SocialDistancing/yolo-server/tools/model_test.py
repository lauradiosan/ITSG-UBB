from ml.yolo import Yolo, Prediction
from config.config import read_config
from PIL import Image, ImageDraw
from util.image import draw_rectangles
import sys
import time
import pydarknet
from typing import List
from util.distance import euclidean_distance
from os import listdir
from os.path import isfile, join


def get_model() -> Yolo:
    yolo_config = read_config('resources/yolo_config.json')
    model = Yolo(yolo_config['weights_path'],
                 yolo_config['config_path'], yolo_config['labels_path'])

    return model


def draw_rectangles_from_predictions(image: Image, predictions: List[Prediction]) -> Image:
    bounding_boxes = [prediction.bounding_box for prediction in predictions]
    return draw_rectangles(image, bounding_boxes)


def get_distances_from_predictions(image: Image, predictions: List[Prediction]):
    for i, p1 in enumerate(predictions, start=0):
        for _, p2 in enumerate(predictions[i + 1:]):
            colors = ['red', 'orange', 'yellow', 'green', 'blue',
                      'purple', 'brown', 'magenta', 'tan', 'cyan']
            distance = euclidean_distance(p1.center, p2.center)
            print(p1, p2, distance)
            if distance < 6912:
                draw = ImageDraw.Draw(image)
                color = colors[i % len(colors)]
                draw.line((p1.center, p2.center), fill=color)

    return image


def run_model(image_path: str):
    model = get_model()
    image = Image.open(image_path).convert('RGB')
    image.load()
    start = time.time()
    result = model.predict(image)
    print('Found {} pedestrians: '.format(len(result)))
    rect_img = draw_rectangles_from_predictions(image, result)
    end = time.time()
    print('\n\nIt took {:.3f}'.format(end - start),
          'seconds to detect the objects in the image.\n')
    rect_img = get_distances_from_predictions(rect_img, result)
    rect_img.show()


def benchmark(images_path: str, max_images=60):
    all_files = [join(images_path, f) for f in listdir(
        images_path) if isfile(join(images_path, f))]

    image_files = [f for f in all_files if '.png' in f]
    print(all_files)
    model = get_model()

    total_time = 0.0
    for i in range(0, max_images):
        image_file = image_files[i]
        image = Image.open(image_file).convert('RGB')
        image.load()
        start = time.time()
        result = model.predict(image)
        #rect_img = draw_rectangles_from_predictions(image, result)
        end = time.time()
        total_time = total_time + (end - start)
        print('Found {} pedestrians\n'.format(len(result)))
        print('It took {:.3f}'.format(end - start),
              'seconds to detect the objects in the image.\n')
        print('Current time so far: {:.3f}'.format(total_time))
        #rect_img = get_distances_from_predictions(rect_img, result)
        # rect_img.show()


if __name__ == '__main__':
    run_model(sys.argv[1])
