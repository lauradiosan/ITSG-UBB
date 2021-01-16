import base64
from io import BytesIO

import re

from PIL import Image


def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'=' * (4 - missing_padding)
    return base64.b64decode(data, altchars)


def encode_image_base64(image: Image):
    """
    Encodes a given PIL image to a base64 string.
    :param image: The image to be encoded.
    :return: the encoded image string.
    """
    buffered = BytesIO()
    image.save(buffered, format='JPEG')
    buffered.seek(0)
    img_bytes = buffered.read()
    base64_encoded_result_bytes = base64.b64encode(img_bytes)
    base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
    return base64_encoded_result_str
