from pathlib import Path

import tensorflow as tf
import os

from keras.models import Model, load_model
from keras.layers import Input, BatchNormalization, Activation, Dense, Dropout
from keras.layers.core import Lambda, RepeatVector, Reshape
from keras.layers.convolutional import Conv2D, Conv2DTranspose
from keras.layers.pooling import MaxPooling2D, GlobalMaxPool2D
from keras.layers.merge import concatenate, add
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from PIL import Image as PilImage
import numpy as np
from skimage import transform


class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class AIManagerBase:
    def __init__(self):
        self._model = None
        self._buildModel()

    def _buildModel(self):
        input_img = Input((128, 128, 1), name='img')
        self._model = self._get_unet(input_img, n_filters=16, dropout=0.05, batchnorm=True)
        self._model.compile(optimizer=Adam(), loss="binary_crossentropy", metrics=["accuracy"])
        model_path = "D:\Anca\manaBionica\master\sem3\ITSG- Bunastare sociala\DjangoMedical\DjangoMedical\medicalHelper\prostateHelper\model-prostate.h5"
        self._model.load_weights(model_path)

    def _conv2d_block(self, input_tensor, n_filters, kernel_size=3, batchnorm=True):
        """Function to add 2 convolutional layers with the parameters passed to it"""
        # first layer
        x = Conv2D(filters=n_filters, kernel_size=(kernel_size, kernel_size),
                   kernel_initializer='he_normal', padding='same')(input_tensor)
        if batchnorm:
            x = BatchNormalization()(x)
        x = Activation('relu')(x)

        # second layer
        x = Conv2D(filters=n_filters, kernel_size=(kernel_size, kernel_size),
                   kernel_initializer='he_normal', padding='same')(x)
        if batchnorm:
            x = BatchNormalization()(x)
        x = Activation('relu')(x)

        return x

    def _get_unet(self, input_img, n_filters=16, dropout=0.1, batchnorm=True):
        """Function to define the UNET Model"""
        # Contracting Path
        c1 = self._conv2d_block(input_img, n_filters * 1, kernel_size=3, batchnorm=batchnorm)
        p1 = MaxPooling2D((2, 2))(c1)
        p1 = Dropout(dropout)(p1)

        c2 = self._conv2d_block(p1, n_filters * 2, kernel_size=3, batchnorm=batchnorm)
        p2 = MaxPooling2D((2, 2))(c2)
        p2 = Dropout(dropout)(p2)

        c3 = self._conv2d_block(p2, n_filters * 4, kernel_size=3, batchnorm=batchnorm)
        p3 = MaxPooling2D((2, 2))(c3)
        p3 = Dropout(dropout)(p3)

        c4 = self._conv2d_block(p3, n_filters * 8, kernel_size=3, batchnorm=batchnorm)
        p4 = MaxPooling2D((2, 2))(c4)
        p4 = Dropout(dropout)(p4)

        c5 = self._conv2d_block(p4, n_filters=n_filters * 16, kernel_size=3, batchnorm=batchnorm)

        # Expansive Path
        u6 = Conv2DTranspose(n_filters * 8, (3, 3), strides=(2, 2), padding='same')(c5)
        u6 = concatenate([u6, c4])
        u6 = Dropout(dropout)(u6)
        c6 = self._conv2d_block(u6, n_filters * 8, kernel_size=3, batchnorm=batchnorm)

        u7 = Conv2DTranspose(n_filters * 4, (3, 3), strides=(2, 2), padding='same')(c6)
        u7 = concatenate([u7, c3])
        u7 = Dropout(dropout)(u7)
        c7 = self._conv2d_block(u7, n_filters * 4, kernel_size=3, batchnorm=batchnorm)

        u8 = Conv2DTranspose(n_filters * 2, (3, 3), strides=(2, 2), padding='same')(c7)
        u8 = concatenate([u8, c2])
        u8 = Dropout(dropout)(u8)
        c8 = self._conv2d_block(u8, n_filters * 2, kernel_size=3, batchnorm=batchnorm)

        u9 = Conv2DTranspose(n_filters * 1, (3, 3), strides=(2, 2), padding='same')(c8)
        u9 = concatenate([u9, c1])
        u9 = Dropout(dropout)(u9)
        c9 = self._conv2d_block(u9, n_filters * 1, kernel_size=3, batchnorm=batchnorm)

        outputs = Conv2D(1, (1, 1), activation='sigmoid')(c9)
        model = Model(inputs=[input_img], outputs=[outputs])
        return model

    def _load_and_resize(self, input_path):
        np_image = PilImage.open(input_path)
        np_image = np.array(np_image).astype('float32') / 255
        np_image = transform.resize(np_image, (128, 128, 1))
        np_image = np.expand_dims(np_image, axis=0)
        return np_image

    def predict_image(self, input_path):
        input_array = self._load_and_resize(input_path)
        output_array = self._model.predict(input_array)
        return self._to_simple_arr(input_array), self._to_simple_arr(output_array)

    def _to_simple_arr(self, arr):
        arr = np.squeeze(arr, axis=0)
        arr = arr[:, :, 0]
        arr = arr * 255
        arr = arr.astype(np.uint8)
        return arr

class AIManager(Singleton, AIManagerBase):
    pass
