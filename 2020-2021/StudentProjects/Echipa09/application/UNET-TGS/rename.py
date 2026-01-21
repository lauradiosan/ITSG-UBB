import os 


# Function to rename multiple files
def rename():

    path = "C:\\Users\\ncoma\\Desktop\\ICA\\bunastareSociala\\UNET-TGS\\masks\\"
    for count, filename in enumerate(os.listdir(path)):
        src = path + filename
        dst = src.replace("segmentation_", "")

        # rename() function will
        # rename all the files
        os.rename(src, dst)


# Driver Code 
rename()
