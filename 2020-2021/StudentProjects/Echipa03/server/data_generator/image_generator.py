from operator import itemgetter

import dicom
from pydicom import dcmread
import os
from scipy import ndimage
import numpy as np
import dicom_numpy
import nrrd
from skimage.transform import resize
import matplotlib.pyplot as plt
from server.utils.config import ROWS, COLS, DEPTH, CHANNELS


def dicom_to_np_array(path):
    """
     Convert a dcm image that stores multiple dcm slices to a np array
     :param path: the path to the director with the dicom file
     :return: np array that correspond to the dcm slices
    """
    files = [os.path.join(path, fname)
             for fname in os.listdir(path) if fname.endswith('.dcm')]
    dcm = dcmread(files[0])
    size = len(dcm.pixel_array[:, 0, 0])
    start = int(size / 4)
    result = np.empty((start, ROWS, COLS, CHANNELS))
    result_index = 0
    for ind in range(start * 2, start * 3):  # choose between segmentation type
        img_resized = resize_image(dcm.pixel_array[ind, :, :])
        result[result_index] = np.expand_dims(img_resized, axis=2)
        result_index = result_index + 1
    return result


def dicom_file_to_np_array(path):
    """
     Combine together all the dicom from the path dir
     :param path: the path to the director with the dicom file
     :return: np array that correspond to the dcm slices
    """
    files = [os.path.join(path, fname)
             for fname in os.listdir(path) if fname.endswith('.dcm')]

    # Read slices as a list before sorting
    dcm_slices = [dicom.read_file(fname) for fname in files]
    array, ijk_to_xyz = dicom_numpy.combine_slices(dcm_slices, True)
    return array


def resize_array(array, x=ROWS, y=COLS, z=DEPTH, channels=CHANNELS):
    return resize(array, (z, x, y, channels), anti_aliasing=True)


def resize_image(array, x=ROWS, y=COLS):
    return resize(array, (x, y), mode='edge', anti_aliasing=False, anti_aliasing_sigma=None, preserve_range=True, order=0)


def data_size(dir_path):
    dicom_dirs = []
    for dir_name in os.listdir(dir_path):
        dicom_dirs.append(os.path.join(dir_path, dir_name))

    size = 0
    for path in dicom_dirs:
        files = [os.path.join(path, fname)
                 for fname in os.listdir(path) if fname.endswith('.dcm')]
        size = size + len(files)

    return size


def read_dicom_input_data(dir_path, size):
    """
    Read the input data and build a np array with all the dcm files
    :param size: the number of input images
    :param dir_path: input dir path
    :return: input data set as np array
    """
    dicom_dirs = []  # create an empty list
    for dir_name in os.listdir(dir_path):
        dicom_dirs.append(os.path.join(dir_path, dir_name))

    dim = (size, ROWS, COLS, CHANNELS)
    result = np.zeros(dim, dtype=float)
    index = 0
    for d in dicom_dirs:
        slices = read_dcm_slices(d)
        for i in range(len(slices)):
            result[index] = np.expand_dims(slices[i, :, :], axis=2)
            index = index + 1
    return result


def read_dicom_target_data(dir_path, size):
    """
     Read the target data(masks) and build a np array with all the dcm files
     :param size: the number of input images
     :param dir_path: masks dir path
     :return: target data set as np array
     """
    dicom_dirs = []  # create an empty list
    for dir_name in os.listdir(dir_path):
        dicom_dirs.append(os.path.join(dir_path, dir_name))

    dim = (size, ROWS, COLS, CHANNELS)
    result = np.zeros(dim, dtype=float)
    index = 0
    for d in dicom_dirs:
        slices = dicom_to_np_array(d)
        for i in range(len(slices)):
            result[index] = slices[i, :, :, :]
            index = index + 1
    return result


def thru_plane_position(dcm):
    """Gets spatial coordinate of image origin whose axis
    is perpendicular to image plane.
    """
    orientation = tuple((float(o) for o in dcm.ImageOrientationPatient))
    position = tuple((float(p) for p in dcm.ImagePositionPatient))
    rowvec, colvec = orientation[:3], orientation[3:]
    normal_vector = np.cross(rowvec, colvec)
    slice_pos = np.dot(position, normal_vector)
    return slice_pos


def read_dcm_slices(path):
    files = [os.path.join(path, fname)
             for fname in os.listdir(path) if fname.endswith('.dcm')]

    # Read slices as a list before sorting
    dcm_slices = [dicom.read_file(fname) for fname in files]

    # Extract position for each slice to sort and calculate slice spacing
    dcm_slices = [(dcm, thru_plane_position(dcm)) for dcm in dcm_slices]
    dcm_slices = sorted(dcm_slices, key=itemgetter(1))
    spacings = np.diff([dcm_slice[1] for dcm_slice in dcm_slices])
    slice_spacing = np.mean(spacings)

    # All slices will have the same in-plane shape
    shape = (ROWS, COLS)
    nslices = len(dcm_slices)

    # Final 3D array will be N_Slices x Columns x Rows
    shape = (nslices, *shape)
    img = np.empty(shape, dtype='float32')
    for idx, (dcm, _) in enumerate(dcm_slices):
        # Rescale and shift in order to get accurate pixel values
        if _requires_rescaling(dcm):
            slope = float(dcm.RescaleSlope)
            intercept = float(dcm.RescaleIntercept)
            img[idx, ...] = dcm.pixel_array.astype('float32') * slope + intercept

        image_2d = resize_image(dcm.pixel_array.astype(np.float32))
        # normalize image
        minimum = np.min(image_2d)
        maximum = np.max(image_2d)
        if maximum > minimum:
            image_2d_scaled = (image_2d - minimum) / (maximum - minimum)
        else:
            image_2d_scaled = image_2d * 0.
        img[idx, ...] = image_2d_scaled

    return img


def _requires_rescaling(dataset):
    return hasattr(dataset, 'RescaleSlope') or hasattr(dataset, 'RescaleIntercept')


def resample(image, scan, new_spacing=[1, 1, 1]):
    # Determine current pixel spacing
    spacing = map(float, ([scan[0].SliceThickness] + scan[0].PixelSpacing))
    spacing = np.array(list(spacing))

    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor

    image = ndimage.interpolation.zoom(image, real_resize_factor)

    return image, new_spacing


def read_nrrd_input_data(path):
    """
    Read the input data and build a np array with all the nrrd files
    :param dir_path: input dir path
    :return: input data set as np array
    """
    dirs = []  # create an empty list
    for dir_name in os.listdir(path):
        dirs.append(os.path.join(path, dir_name))

    files = []
    for dir_path in dirs:
        files_dir = [os.path.join(dir_path, fname)
                     for fname in os.listdir(dir_path) if fname.endswith('.nrrd') and fname.upper().find('AX T2') != -1]
        files.extend(files_dir)

    dim = (len(files) * 50, ROWS, COLS, CHANNELS)
    result = np.zeros(dim, dtype=float)
    index = 0
    for d in files[:1]:
        input_data = nrrd.read(d)[0]
        for ind in range(10, input_data.shape[2] - 10):
            resized_image = resize_image(input_data[:, :, ind])
            result[index] = resized_image[:, :, np.newaxis]
            plt.imshow(input_data[:, :, ind], cmap=plt.cm.bone)
            plt.show()
            index = index + 1

    return result


def read_nrrd_target_data(path):
    """
    Read the input data and build a np array with all the nrrd files
    :param dir_path: input dir path
    :return: input data set as np array
    """
    dirs = []  # create an empty list
    for dir_name in os.listdir(path):
        dirs.append(os.path.join(path, dir_name))

    files = []
    for dir_path in dirs:
        files_dir = [os.path.join(dir_path, fname)
                     for fname in os.listdir(dir_path) if fname.endswith('.nrrd') and fname.lower().find('segmentation.seg') != -1]
        files.extend(files_dir)

    dim = (len(files) * 50, ROWS, COLS, CHANNELS)
    result = np.zeros(dim, dtype=float)
    index = 0
    for d in files[:1]:
        input_data = nrrd.read(d)[0][0]  # take the cancer segmentation
        for ind in range(input_data.shape[2]):
            resized_image = resize_image(input_data[:, :, ind])
            result[index] = resized_image[:, :, np.newaxis]
            plt.imshow(input_data[:, :, ind], cmap=plt.cm.bone)
            plt.show()
            index = index + 1

    return result


def read_nrrd_input(path):
    return nrrd.read(path)


def read_nrrd_target(path):
    seg = nrrd.read(path)
