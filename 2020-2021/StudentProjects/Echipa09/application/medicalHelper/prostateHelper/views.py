from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from prostateHelper.forms import LoadImageForm
from prostateHelper.models import Image

from PIL import Image as PilImage, ImageFilter
import base64
import numpy as np
from io import BytesIO

from .ai_helper import AIManager

ai_manager = AIManager()


def index(request):
    if request.method == 'POST':
        form = LoadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_id = form.save().id
            return HttpResponseRedirect(reverse('prostateHelper:analysed_image', args=(image_id,)))
    else:
        form = LoadImageForm()
    return render(request, 'prostateHelper/index.html', {'form': form})


def process(original):
    return ai_manager.predict_image(original)


def analysed_image(request, image_id):
    if request.method == 'GET':
        try:
            im = Image.objects.get(pk=image_id)
            input_array, output_array = process(im.original)
            mask_uri, result_uri = convert_array_to_uri(input_array, output_array)
        except Image.DoesNotExist:
            raise Http404("Image does not exist")
        return render(request, 'prostateHelper/analysed_image.html',
                      {'image': im,
                       'mask_uri': mask_uri,
                       'result_uri': result_uri})


def convert_array_to_uri(input_arr, mask_arr):
    img = PilImage.fromarray(input_arr).convert('L').convert('RGB')
    mask = PilImage.fromarray(mask_arr).convert('L')

    mainN = np.array(img)
    mainN = drawContour(mainN, mask, (255, 0, 0))  # draw contour 1 in red

    res = PilImage.fromarray(mainN)
    return from_pil_image_to_uri(mask), from_pil_image_to_uri(res)


def from_pil_image_to_uri(image):
    data = BytesIO()
    image.save(data, "JPEG")  # pick your format
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,' + data64.decode('utf-8')


def drawContour(m, s, RGB):
    """Draw edges of contour 'c' from segmented image 's' onto 'm' in colour 'RGB'"""
    # Fill contour "c" with white, make all else black
    thisContour = s.point(lambda p: p > 125 and 255)
    # DEBUG: thisContour.save(f"interim{c}.png")

    # Find edges of this contour and make into Numpy array
    thisEdges = thisContour.filter(ImageFilter.FIND_EDGES)
    thisEdgesN = np.array(thisEdges)

    # Paint locations of found edges in color "RGB" onto "main"
    m[np.nonzero(thisEdgesN)] = RGB
    return m
