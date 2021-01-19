import numpy as np  # (pip install numpy)
from skimage import measure  # (pip install scikit-image)
from shapely.geometry import Polygon, MultiPolygon  # (pip install Shapely)
import os
import json
from numpy import asarray
from PIL import Image, ImageDraw

class CocoUtils:
    def create_sub_masks(self, mask_image, width, height):
        # Initialize a dictionary of sub-masks indexed by RGB colors
        sub_masks = {}
        for x in range(width):
            for y in range(height):
                # Get the RGB values of the pixel
                pixel = mask_image.getpixel((x, y))[:3]

                # If the pixel is not black...
                if pixel != (0, 0, 0):
                    # Check to see if we've created a sub-mask...
                    pixel_str = str(pixel)
                    sub_mask = sub_masks.get(pixel_str)
                    if sub_mask is None:
                        # Create a sub-mask (one bit per pixel) and add to the dictionary
                        # Note: we add 1 pixel of padding in each direction
                        # because the contours module doesn't handle cases
                        # where pixels bleed to the edge of the image
                        sub_masks[pixel_str] = Image.new('1', (width + 2, height + 2))

                    # Set the pixel value to 1 (default is 0), accounting for padding
                    sub_masks[pixel_str].putpixel((x + 1, y + 1), 1)

        return sub_masks

    def create_sub_mask_annotation(self, sub_mask):
        # Find contours (boundary lines) around each sub-mask
        # Note: there could be multiple contours if the object
        # is partially occluded. (E.g. an elephant behind a tree)
        contours = measure.find_contours(sub_mask, 0.5, positive_orientation='low')

        polygons = []
        segmentations = []
        j = 0
        for contour in contours:
            # Flip from (row, col) representation to (x, y)
            # and subtract the padding pixel
            for i in range(len(contour)):
                row, col = contour[i]
                contour[i] = (col - 1, row - 1)

            # Make a polygon and simplify it
            poly = Polygon(contour)
            poly = poly.simplify(1.0, preserve_topology=False)

            if (poly.is_empty):
                # Go to next iteration, dont save empty values in list
                continue

            polygons.append(poly)

            segmentation = np.array(poly.exterior.coords).ravel().tolist()
            segmentations.append(segmentation)

        return polygons, segmentations

    def create_image_annotation(self, file_name, width, height, image_id):
        images = {
            'file_name': file_name,
            'height': height,
            'width': width,
            'id': image_id
        }

        return images

    # Helper function to get absolute paths of all files in a directory
    def absolute_file_paths(self, directory):
        mask_images = []

        for root, dirs, files in os.walk(os.path.abspath(directory)):
            for file in files:
                # Filter only for images in folder
                if '.png' or '.jpg' in file:
                    mask_images.append(os.path.join(root, file))
        return mask_images

    def create_annotation_format(self, polygon, segmentation, image_id, category_id, annotation_id):
        min_x, min_y, max_x, max_y = polygon.bounds
        width = max_x - min_x
        height = max_y - min_y
        bbox = (min_x, min_y, width, height)
        area = polygon.area

        annotation = {
            'segmentation': segmentation,
            'area': area,
            'iscrowd': 0,
            'image_id': image_id,
            'bbox': bbox,
            'category_id': category_id,
            'id': annotation_id
        }

        return annotation

    def images_annotations_info(self, maskpath, category_ids):
        # This id will be automatically increased as we go
        annotation_id = 1

        annotations = []
        images = []

        # Get absolute paths of all files in a directory
        mask_images = self.absolute_file_paths(maskpath)

        for image_id, mask_image in enumerate(mask_images, 1):
            file_name = os.path.basename(mask_image).split('.')[0] + ".png"

            # image shape
            mask_image_open = Image.open(mask_image)
            w, h = mask_image_open.size

            # 'images' info
            image = self.create_image_annotation(file_name, w, h, image_id)
            images.append(image)

            sub_masks = self.create_sub_masks(mask_image_open, w, h)
            for color, sub_mask in sub_masks.items():
                if color in category_ids:
                    category_id = category_ids[color]

                    # 'annotations' info
                    polygons, segmentations = self.create_sub_mask_annotation(asarray(sub_mask))

                    # Three labels are multipolygons in our case: wall, roof and sky
                    if (category_id == 2 or category_id == 5 or category_id == 6):
                        # Combine the polygons to calculate the bounding box and area
                        multi_poly = MultiPolygon(polygons)

                        annotation = self.create_annotation_format(multi_poly, segmentations, image_id, category_id, annotation_id)

                        annotations.append(annotation)
                        annotation_id += 1
                    else:
                        for i in range(len(polygons)):
                            # Cleaner to recalculate this variable
                            segmentation = [np.array(polygons[i].exterior.coords).ravel().tolist()]

                            annotation = self.create_annotation_format(polygons[i], segmentation, image_id, category_id,
                                                                  annotation_id)

                            annotations.append(annotation)
                            annotation_id += 1

        return images, annotations

    def pngToCoco(self, mask_path):
        # Create the annotations of the ECP dataset (Coco format)
        coco_format = {
            "images": [
                {
                }
            ],
            "categories": [
                {
                    "supercategory": "prostate",
                    "id": 1,
                    "name": 'prostate'
                },

            ],
            "annotations": [
                {
                }
            ]
        }

        # Define which colors match which categories in the images
        category_ids = {
            '(253, 231, 36)': 1,  # Prostate
        }

        coco_format['images'], coco_format['annotations'] = self.images_annotations_info(mask_path, category_ids)
        # print(json.dumps(coco_format))
        with open('{}.json'.format("mask"), 'w+') as outfile:
            json.dump(coco_format, outfile)


    def polygon_to_mask(self, polygon_points, width, height):
        img = Image.new('L', (width, height), 0)
        ImageDraw.Draw(img).polygon(polygon_points, outline=1, fill=1)
        mask = np.array(img)
        return mask


    def json_annotation_to_masks(self, json_file):
        file = open(json_file, "r")
        info = json.loads(file.read())
        file.close()

        height = info["imageHeight"]
        width = info["imageWidth"]

        masks = []

        for shape in info["shapes"]:
            polygon_points = []
            for [x, y] in shape["points"]:
                polygon_points.append((int(x), int(y)))

            mask = self.polygon_to_mask(polygon_points, width, height)
            masks.append(mask)

        return masks
