from __future__ import division, print_function

import numpy as np
import tensorflow as tf
from keras.callbacks import LearningRateScheduler
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

from server.data_generator.image_generator import data_size, read_dicom_input_data, read_dicom_target_data
from server.model_with_generator.metrics import dice_coef_loss, dice_coef
from server.model_with_generator.models import UNet
from server.utils.config import INPUT_PATH, MASK_PATH, ROWS, COLS, PATH

physical_devices = tf.config.experimental.list_physical_devices('GPU')
assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
config = tf.config.experimental.set_memory_growth(physical_devices[0], True)


def dicom_to_array(img_rows, img_cols):
    size = data_size(INPUT_PATH)
    images = read_dicom_input_data(INPUT_PATH, size)
    masks = read_dicom_target_data(MASK_PATH, size)

    # I will do only binary classification for now
    # img_masks = np.array(img_masks>0.45, dtype=int)
    l = len(images)
    size = int(75 * l / 100)

    train_images = images[:size - 1]
    train_masks = masks[:size - 1]

    val_images = images[size:l - 5]
    val_masks = masks[size:l - 5]

    test_images = images[l - 5:l]
    test_masks = masks[l - 5:l]

    np.save(PATH + 'train' + '.npy', train_images)
    np.save(PATH + 'train' + '_masks.npy', train_masks)
    np.save(PATH + 'validate' + '.npy', val_images)
    np.save(PATH + 'validate' + '_masks.npy', val_masks)
    np.save(PATH + 'test' + '.npy', test_images)
    np.save(PATH + 'test' + '_masks.npy', test_masks)


def load_data():
    X_train = np.load(PATH + 'train.npy')
    y_train = np.load(PATH + 'train_masks.npy')
    X_test = np.load(PATH + 'test.npy')
    y_test = np.load(PATH + 'test_masks.npy')
    X_val = np.load(PATH + 'validate.npy')
    y_val = np.load(PATH + 'validate_masks.npy')

    return X_train, y_train, X_test, y_test, X_val, y_val


# learning rate schedule
def step_decay(epoch):
    initial_lrate = 0.001
    drop = 0.5
    epochs_drop = 5
    lrate = initial_lrate * drop ** int((1 + epoch) / epochs_drop)
    return lrate


def keras_fit_generator(img_rows=ROWS, img_cols=ROWS, n_imgs=10 ** 4, batch_size=32, regenerate=True):
    if regenerate:
        dicom_to_array(img_rows, img_cols)
        # preprocess_data()

    X_train, y_train, X_test, y_test, X_val, y_val = load_data()

    img_rows = X_train.shape[1]
    img_cols = img_rows

    # we create two instances with the same arguments
    data_gen_args = dict(
        featurewise_center=False,
        featurewise_std_normalization=False,
        rotation_range=90.,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        vertical_flip=True,
        zoom_range=0.2)  # ,
    # preprocessing_function=elastic_transform)

    image_datagen = ImageDataGenerator(**data_gen_args)
    mask_datagen = ImageDataGenerator(**data_gen_args)

    # Provide the same seed and keyword arguments to the fit and flow methods
    seed = 1
    image_datagen.fit(X_train, seed=seed)
    mask_datagen.fit(y_train, seed=seed)

    image_generator = image_datagen.flow(X_train, batch_size=batch_size, seed=seed)

    mask_generator = mask_datagen.flow(y_train, batch_size=batch_size, seed=seed)

    train_generator = zip(image_generator, mask_generator)

    model = UNet((img_rows, img_cols, 1), start_ch=8, depth=7, batchnorm=True, dropout=0.5, maxpool=True, residual=True)
    # model.load_weights('../data/weights.h5')

    model.summary()
    model_checkpoint = ModelCheckpoint(
        '../data/weights.h5', monitor='val_loss', save_best_only=True)

    lrate = LearningRateScheduler(step_decay)

    model.compile(optimizer=Adam(), loss=dice_coef_loss, metrics=[dice_coef, 'binary_accuracy'])
    # model = UNet2DModel(rows=ROWS, columns=COLS, number_of_channels=CHANNELS, dropout=DROPOUT, decay=UNET_DECAY, learning_rate=LEARNING_RATE)
    # model = model.build_UNet2D_model()

    model.fit_generator(
        train_generator,
        steps_per_epoch=25,
        epochs=100,
        verbose=1,
        shuffle=True,
        validation_data=(X_val, y_val),
        callbacks=[model_checkpoint, lrate])

    score = model.evaluate(X_test, y_test, verbose=2)

    print()
    print('Test accuracy:', score[1])


import time

start = time.time()
keras_fit_generator(img_rows=ROWS, img_cols=COLS, regenerate=False, n_imgs=100, batch_size=2)

end = time.time()

print('Elapsed time:', round((end - start) / 60, 2))
