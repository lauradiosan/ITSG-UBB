from io import BytesIO
from typing import Dict, List, Tuple
from PIL import Image, ImageDraw
import numpy as np

from util.encoding import decode_base64


def image_from_json(json_data: Dict[str, str]) -> Image:
    image_base64 = json_data['image']
    image_base64 = bytes(image_base64, encoding="ascii")
    image_data = Image.open(BytesIO(decode_base64(image_base64)))
    return image_data


def draw_rectangles(image: Image, rects: List[Tuple[int, int, int, int]], size=None) -> Image:
    if size:
        image = image.resize(size=size)

    outline_colors = ['red', 'orange', 'yellow', 'green', 'blue',
                      'purple', 'brown', 'magenta', 'tan', 'cyan']
    for index, rect in enumerate(rects):
        x1, y1, x2, y2 = rect
        draw = ImageDraw.Draw(image)
        outline_color = outline_colors[index % len(outline_colors)]
        draw.rectangle(((x1, y1), (x2, y2)), outline=outline_color, width=5)

    return image
