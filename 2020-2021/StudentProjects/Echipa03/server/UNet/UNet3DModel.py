from keras import Model
from keras.layers import Input, MaxPooling3D
from keras import backend as K
from keras.layers.convolutional import Conv3D, Deconv3D
from keras.layers.core import Dropout, Lambda
from keras.layers.merge import concatenate
from keras.optimizers import SGD

from server.utils.config import PIXEL_MEAN, MIN_BOUND, MAX_BOUND

K.set_image_data_format('channels_last')


def iou_coef(y_true, y_pred, smooth=1):
    intersection = K.sum(y_true * y_pred, axis=[1, 2, 3, 4])
    union = K.sum(y_true, [1, 2, 3, 4]) + K.sum(y_pred, [1, 2, 3, 4]) - intersection
    iou = K.mean((intersection + smooth) / (union + smooth), axis=0)
    return iou


def dice_coef(y_true, y_pred, smooth=1):
    intersection = K.sum(y_true * y_pred, axis=[1, 2, 3, 4])
    union = K.sum(y_true, axis=[1, 2, 3, 4]) + K.sum(y_pred, axis=[1, 2, 3, 4])
    dice = K.mean((2. * intersection + smooth) / (union + smooth), axis=0)
    return dice


def iou_coef_loss(yt, yp, smooth=1):
    return 1 - iou_coef(yt, yp, smooth)


def dice_coef_loss(yt, yp, smooth=1):
    return 1 - dice_coef(yt, yp, smooth)


def zero_center(image):
    image = image - PIXEL_MEAN
    return image


def normalize(image):
    image = (image - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
    image[image > 1] = 1.
    image[image < 0] = 0.
    return image


class UNet3DModel:
    def __init__(self, rows, columns, number_of_channels, depth, dropout, decay, learning_rate):
        self.number_of_rows = rows
        self.number_of_cols = columns
        self.depth = depth
        self.channels = number_of_channels
        self.dropout_rate = dropout
        self.weight_decay = decay
        self.learning_rate = learning_rate

    def build_UNet3D_model(self):
        print("Build U-Net model")

        # Build U-Net model
        inputs = Input((self.depth, self.number_of_cols, self.number_of_cols, self.channels))
        s = Lambda(lambda x: x / 255)(inputs)

        c1 = Conv3D(64, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(s)
        c1 = Dropout(self.dropout_rate)(c1)
        c1 = Conv3D(64, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
        p1 = MaxPooling3D((2, 2, 2))(c1)

        c2 = Conv3D(128, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p1)
        c2 = Dropout(self.dropout_rate)(c2)
        c2 = Conv3D(128, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
        p2 = MaxPooling3D((2, 2, 2))(c2)

        c3 = Conv3D(256, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p2)
        c3 = Dropout(self.dropout_rate)(c3)
        c3 = Conv3D(256, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c3)
        p3 = MaxPooling3D((2, 2, 2))(c3)

        c4 = Conv3D(512, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p3)
        c4 = Dropout(self.dropout_rate)(c4)
        c4 = Conv3D(512, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c4)
        p4 = MaxPooling3D(pool_size=(2, 2, 2))(c4)

        c5 = Conv3D(512, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p4)
        c5 = Dropout(self.dropout_rate)(c5)
        c5 = Conv3D(512, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c5)

        u6 = Deconv3D(512, (2, 2, 2), strides=(2, 2, 2), padding='same')(c5)
        u6 = concatenate([u6, c4])
        c6 = Conv3D(256, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u6)
        c6 = Dropout(self.dropout_rate)(c6)
        c6 = Conv3D(256, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c6)

        u7 = Deconv3D(256, (2, 2, 2), strides=(2, 2, 2), padding='same')(c6)
        u7 = concatenate([u7, c3])
        c7 = Conv3D(128, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u7)
        c7 = Dropout(self.dropout_rate)(c7)
        c7 = Conv3D(128, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c7)

        u8 = Deconv3D(128, (2, 2, 2), strides=(2, 2, 2), padding='same')(c7)
        u8 = concatenate([u8, c2])
        c8 = Conv3D(64, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u8)
        c8 = Dropout(self.dropout_rate)(c8)
        c8 = Conv3D(64, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c8)

        u9 = Deconv3D(64, (2, 2, 2), strides=(2, 2, 2), padding='same')(c8)
        u9 = concatenate([u9, c1])
        c9 = Conv3D(32, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u9)
        c9 = Dropout(self.dropout_rate)(c9)
        c9 = Conv3D(32, (3, 3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c9)

        outputs = Conv3D(1, (1, 1, 1), activation='softmax')(c9)

        optimizer = SGD(lr=self.learning_rate, decay=self.weight_decay)

        model = Model(inputs=[inputs], outputs=[outputs])
        model.compile(optimizer=optimizer, loss=dice_coef_loss,
                      metrics=[iou_coef, dice_coef, "accuracy"])
        return model
