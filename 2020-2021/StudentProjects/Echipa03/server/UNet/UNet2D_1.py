from keras import Model
from keras.layers import Conv2D, Input, MaxPooling2D
from keras import backend as K
from keras.layers.convolutional import Deconv2D
from keras.layers.core import Dropout
from keras.optimizers import SGD
from keras.regularizers import l2
from keras.layers.merge import add

from server.utils.config import DECAY, MOMENTUM

K.set_image_data_format('channels_last')


def dice_coef(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + 1.0) / (K.sum(y_true_f) + K.sum(y_pred_f) + 1.0)


def IoU(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    union = K.sum(y_true_f) + K.sum(y_pred_f) - intersection
    return intersection / union


def dice_coef_loss(y_true, y_pred):
    return 1 - dice_coef(y_true, y_pred)


class UNet2DModel:
    def __init__(self, rows, columns, number_of_channels, dropout, decay, learning_rate):
        self.number_of_rows = rows
        self.number_of_cols = columns
        self.channels = number_of_channels
        self.dropout_rate = dropout
        self.weight_decay = decay
        self.learning_rate = learning_rate

    def build_down_layer(self, layer_input, filters, kernel_size, dropout=True):
        layer = Conv2D(filters=filters, kernel_size=kernel_size, kernel_initializer='he_normal', padding='same',
                       activation='relu',
                       use_bias=False,
                       kernel_regularizer=l2(self.weight_decay))(layer_input)
        if dropout:
            layer = Dropout(self.dropout_rate)(layer)
        layer = Conv2D(filters=filters, kernel_size=kernel_size, kernel_initializer='he_normal', padding='same',
                       activation='relu',
                       use_bias=False,
                       kernel_regularizer=l2(self.weight_decay))(layer)
        return layer

    def build_up_layer(self, layer_input, down_layer, filters, kernel_size, strides):
        up_layer = Deconv2D(filters=filters, kernel_size=kernel_size, strides=strides, activation='relu',
                            padding='same', data_format='channels_last',
                            kernel_initializer='he_normal', kernel_regularizer=l2(self.weight_decay))(layer_input)
        layer = add([up_layer, down_layer])
        return layer

    def build_output_layer(self, layer_input, filters, kernel_size):
        layer = Conv2D(filters=filters, kernel_size=kernel_size, kernel_initializer='he_normal', padding='same',
                       activation='sigmoid', use_bias=False,
                       kernel_regularizer=l2(self.weight_decay))(layer_input)
        return layer

    def build_side_out_layer(self, layer_input, filters, kernel_size, strides):
        up = Deconv2D(filters=filters, kernel_size=kernel_size, strides=strides, activation='relu', padding='same',
                      kernel_initializer='he_normal', kernel_regularizer=l2(self.weight_decay))(layer_input)
        layer = self.build_output_layer(up, 1, (1, 1))
        return layer

    def build_UNet(self):
        if K.image_data_format() == 'channels_last':
            input_layer = Input(shape=(self.number_of_rows, self.number_of_cols, self.channels))
        else:
            input_layer = Input(shape=(self.channels, self.number_of_rows, self.number_of_cols))

        # first layer down
        down_layer1 = self.build_down_layer(layer_input=input_layer, filters=64, kernel_size=(3, 3))
        max_pooling_layer1 = MaxPooling2D((2, 2))(down_layer1)

        # layer 2 down
        down_layer2 = self.build_down_layer(layer_input=max_pooling_layer1, filters=128, kernel_size=(3, 3))
        max_pooling_layer2 = MaxPooling2D((2, 2))(down_layer2)

        # layer 3 down
        down_layer3 = self.build_down_layer(layer_input=max_pooling_layer2, filters=256, kernel_size=(3, 3))
        max_pooling_layer3 = MaxPooling2D((2, 2))(down_layer3)

        # layer 4 down
        down_layer4 = self.build_down_layer(layer_input=max_pooling_layer3, filters=512, kernel_size=(3, 3))
        max_pooling_layer4 = MaxPooling2D((2, 2))(down_layer4)

        # mid layer
        mid_layer = self.build_down_layer(layer_input=max_pooling_layer4, filters=512, kernel_size=(3, 3))

        # layer 4 up
        up_layer4 = self.build_up_layer(layer_input=mid_layer, down_layer=down_layer4, filters=512, kernel_size=(3, 3),
                                        strides=(2, 2))
        up_layer4 = self.build_down_layer(layer_input=up_layer4, filters=256, kernel_size=(3, 3))

        # layer 3 up
        up_layer3 = self.build_up_layer(layer_input=up_layer4, down_layer=down_layer3, filters=256, kernel_size=(3, 3),
                                        strides=(2, 2))
        up_layer3 = self.build_down_layer(layer_input=up_layer3, filters=128, kernel_size=(3, 3))

        # layer 2 up
        up_layer2 = self.build_up_layer(layer_input=up_layer3, down_layer=down_layer2, filters=128, kernel_size=(3, 3),
                                        strides=(2, 2))
        up_layer2 = self.build_down_layer(layer_input=up_layer2, filters=64, kernel_size=(3, 3))

        # layer 1 up
        up_layer1 = self.build_up_layer(layer_input=up_layer2, down_layer=down_layer1, filters=64, kernel_size=(3, 3),
                                        strides=(2, 2))
        up_layer1 = self.build_down_layer(layer_input=up_layer1, filters=32, kernel_size=(3, 3))

        output_layer8 = self.build_output_layer(up_layer1, 1, (1, 1))

        model = Model([input_layer],
                      [output_layer8])
        sgd = SGD(lr=self.learning_rate, decay=DECAY, momentum=MOMENTUM, nesterov=True)
        model.compile(optimizer=sgd,
                      loss=dice_coef_loss,
                      metrics=[dice_coef, "accuracy"])
        return model
