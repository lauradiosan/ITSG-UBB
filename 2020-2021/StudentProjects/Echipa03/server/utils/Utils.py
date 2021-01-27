import nibabel
import trimesh
import matplotlib.pyplot as plt
import pydicom
import os
import numpy as np

from server.utils.config import ROWS, COLS


def make_ax():
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    return ax


def print_img(array):
    ax = make_ax()
    ax.voxels(array, edgecolors='gray', shade=False)
    plt.show()


def stl_to_np_array(path):
    mesh1 = trimesh.load_mesh(path)
    volume = mesh1.voxelized(pitch=0.1)
    mat = volume.matrix  # matrix of boolean
    return mat


def dicom_to_np_array_dataset(pathDicom):
    """
    :type pathDicom: path to a folder containing Dicom images
    :rtype: np array representation of all the dicom images from the provided folder
    """
    lstFilesDCM = []  # create an empty list
    for dirName, subdirList, fileList in os.walk(pathDicom):
        for filename in fileList:
            # if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName, filename))

    # Get ref file
    RefDs = pydicom.read_file(lstFilesDCM[0])
    # Load dimensions based on the number of rows, columns, and slices (along the Z axis)
    ConstPixelDims = (len(lstFilesDCM), ROWS, COLS, 1)
    # Load spacing values (in mm)
    # ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))

    # Load all the pixel data into an appropriate sized NumPy array
    # The array is sized based on 'ConstPixelDims'
    ArrayDicom = np.zeros(ConstPixelDims, dtype=float)
    # loop through all the DICOM files
    for filenameDCM in lstFilesDCM:
        # read the file
        array = pydicom.read_file(filenameDCM).pixel_array
        # array = resize_array(array)
        # plt.imshow(array,  cmap=plt.cm.bone)
        # plt.show()

        array = np.reshape(array, array.shape + (1,))
        # plt.imshow(array, cmap=plt.cm.bone)
        # plt.show()
        ArrayDicom[lstFilesDCM.index(filenameDCM)] = array

    # plt.imshow(ArrayDicom[0], cmap=plt.cm.bone)
    # plt.show()
    return ArrayDicom


def niftiToNpArray(pathToNifti):
    """
    :type pathToNifti: path to a Nifti image
    :rtype: np array representation of all the dicom images from the provided folder
    """
    img = nibabel.load(pathToNifti)
    return np.array(img.dataobj)
