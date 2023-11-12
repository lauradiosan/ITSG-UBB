import os
from PIL import Image


# Function to resize multiple files
def resize():
    path = "C:\\Users\\ncoma\\Desktop\\ICA\\bunastareSociala\\UNET-TGS\\images\\"
    for count, filename in enumerate(os.listdir(path)):
        src = path + filename
        im = Image.open(src)
        # resize from 369x369 -> 128x128
        # 217 * 0.34688346883468834688346883468835 = 128
        downsize_factor = 0.34688346883468834688346883468835
        out = im.resize([int(downsize_factor * s) for s in im.size])
        out.save(str(src))


# Driver Code
resize()
