# if want to run on CPU
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import matplotlib.pyplot as plt
from keras.engine.saving import load_model

from server.UNet.UNet2D_1 import UNet2DModel
from server.UNet.UNet2D_2 import UNet2D_2, dice_coef_loss, dice_coef
from server.UNet.UNet3DModel import UNet3DModel
from data_generator.image_generator import read_dicom_input_data, read_dicom_target_data, data_size
from utils.config import *

train = False
unet_version = 1


def train_model():
    print('Loading train data...')

    size = data_size(INPUT_PATH)
    train_images = read_dicom_input_data(INPUT_PATH, size)
    train_masks = read_dicom_target_data(MASK_PATH, size)

    print('Input data shape', train_images.shape)
    print('Mask data shape', train_masks.shape)
    print('Creating and starting the model...')

    if unet_version == 1:
        model = UNet2DModel(rows=ROWS, columns=COLS, number_of_channels=CHANNELS, dropout=DROPOUT, decay=UNET_DECAY, learning_rate=LEARNING_RATE)
        model = model.build_UNet()
    else:
        model = UNet2D_2(rows=ROWS, columns=COLS, number_of_channels=CHANNELS, dropout=DROPOUT, decay=UNET_DECAY, learning_rate=LEARNING_RATE)
        model = model.build_UNet()
    model.summary()
    model.fit(train_images,
              train_masks,
              batch_size=BATCH_SIZE,
              epochs=EPOCHS,
              verbose=2,
              shuffle=True,
              validation_split=VALIDATION_SPLIT)
    model.save(SAVED_MODEL_PATH)


def train_3D_model():
    print('Loading train data...')

    size = data_size(INPUT_PATH)
    train_images = read_dicom_input_data(INPUT_PATH, size)
    train_masks = read_dicom_target_data(MASK_PATH, size)

    print('Input data shape:')
    print(train_images.shape)
    print('Mask data shape:')
    print(train_masks.shape)

    model = UNet3DModel(rows=ROWS, columns=COLS, number_of_channels=CHANNELS, depth=DEPTH,
                        dropout=DROPOUT, decay=UNET_DECAY, learning_rate=LEARNING_RATE)
    model = model.build_UNet3D_model()
    model.load_weights(SAVED_MODEL_PATH)
    model.summary()
    model.fit(train_images, train_masks,
              batch_size=BATCH_SIZE,
              epochs=EPOCHS,
              verbose=2,
              shuffle=True,
              validation_split=VALIDATION_SPLIT)
    model.save(SAVED_MODEL_PATH)


def predict_and_show_plot(input_folder_path, mask_folder_path):
    print('Loading data...')
    size = data_size(input_folder_path)
    test_images = read_dicom_input_data(input_folder_path, size)
    test_masks = read_dicom_target_data(mask_folder_path, size)
    model = load_model(SAVED_MODEL_PATH, custom_objects={'dice_coef_loss': dice_coef_loss, 'dice_coef': dice_coef})
    loss, acc = model.evaluate(test_images, test_masks, verbose=2)
    print("Restored model, accuracy: {:5.2f}%".format(100 * acc))
    model.summary()
    rez = model.predict(test_images)
    plt.imshow(rez, cmap=plt.cm.bone)
    plt.show()


def predict(input_folder_path):
    print('Loading data...')
    size = data_size(input_folder_path)
    test_images = read_dicom_input_data(input_folder_path, size)
    model = load_model(SAVED_MODEL_PATH, custom_objects={'dice_coef_loss': dice_coef_loss, 'dice_coef': dice_coef})
    rez = model.predict(test_images)
    return rez


if __name__ == '__main__':
    if train:
        train_model()
    else:
        predict_and_show_plot(TEST_PATH, TEST_MASK)
