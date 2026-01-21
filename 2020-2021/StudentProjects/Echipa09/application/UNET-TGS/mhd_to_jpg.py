# code scris urat in cazul in care ne mai trebuie conversia
import os
from os import listdir

import SimpleITK as sitk
import matplotlib.pylab as plt


def to_images(file, path):
    print("Processing file: " + file)
    input_path = path + file
    output_path = path

    file_name = os.path.splitext(file)[0]

    if 'segment' in file_name:
        output_path = output_path + 'Label\\' + file_name
    else:
        output_path = output_path + 'Input\\' + file_name
    
    ct_scans = sitk.GetArrayFromImage(sitk.ReadImage(input_path, sitk.sitkFloat32))
    no_imgs = ct_scans.shape[0]

    for i in range(0, no_imgs):
        plt.imshow(ct_scans[i])
        plt.axis('off')
        sub_name = output_path + '_'+str(i)+'.jpeg'
        plt.savefig(sub_name, bbox_inches='tight', pad_inches=0)


image_folder = "C:\\Users\\ncoma\\Desktop\\ICA\\bunastareSociala\\UNET-TGS\\Train_After\\train\\"

files = [f for f in listdir(image_folder) if '.mhd' in f]
for f in files:
    to_images(f, image_folder)
