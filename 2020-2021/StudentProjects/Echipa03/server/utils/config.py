# input size
ROWS = 256
COLS = 256
DEPTH = 16
CHANNELS = 1

# learning parameters
DECAY = 1e-6
MOMENTUM = 0.9
DROPOUT = 0.3
UNET_DECAY = 5e-4
LEARNING_RATE = 0.0001

VALIDATION_SPLIT = 0.2
BATCH_SIZE = 2
EPOCHS = 100

PIXEL_MEAN = 0.25
MIN_BOUND = -1000.0
MAX_BOUND = 400.0

PATH = "D:\\University\\ITSG\\itsg-socialgoodteam\\server\\data\\"
INPUT_PATH = "D:\\University\\ITSG\\itsg-socialgoodteam\\server\\data\\input"
MASK_PATH = "D:\\University\\ITSG\\itsg-socialgoodteam\\server\\data\\mask"
SAVED_MODEL_PATH = "D:\\University\\ITSG\\itsg-socialgoodteam\\server\\saved_model\\saved_model.h5" #"D:\\Proiecte\\Python\\itsg-socialgoodteam\\Server\\saved_model\\saved_model.h5"
TEST_PATH = "D:\\University\\ITSG\\itsg-socialgoodteam\\server\\data\\test\\input"
TEST_MASK = "D:\\University\\ITSG\\itsg-socialgoodteam\\server\\data\\test\\mask" #"D:\\Proiecte\\ImaginiMedicale\\ProstateDataset\\axial\\test"
