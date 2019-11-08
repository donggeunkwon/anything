# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 17:47:58 2019

    main

@author: Donggeun Kwon (donggeun.kwon@gmail.com)

Cryptographic Algorithm Lab.
Graduate School of Information Security, Korea University

"""

# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

from ImageLoader import Loader
from ImageNet import Resnet
from CustomBack import TrainValTensorBoard

import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from datetime import datetime
import scipy
import scipy.io

# parameters
IMG_PATH = os.getcwd()
DEPTH = 1
BATCH_SIZE = 100
EPOCHS = 200
NOW = datetime.now()


NUM_DEPTH_NET = 9 * DEPTH + 2


def main():   
    ### load dataset
    ld = Loader(IMG_PATH) 
    xtrain, ytrain = ld.load_train_img()
    xvalid, yvalid = ld.load_valid_img()
    ytrain, yvalid = ld.one_hot(ytrain), ld.one_hot(yvalid)
    
    ### set image network
	img_shape = (ld.IMAGE_SIZE, ld.IMAGE_SIZE, ld.NUM_CHANNELS)
    ImgNet = Resnet(input_shape=img_shape, 
                    depth=NUM_DEPTH_NET, 
                    num_classes=ld.NUM_CLASSES)
    
    ImgNet.compile(optimizer=tf.keras.optimizers.Adam(lr=1e-3, 
                                                      epsilon=1.0), 
                   loss=tf.keras.losses.categorical_crossentropy, 
                   metrics=['acc'])
    ImgNet.summary()
    
    ### callback options
    cb_check = tf.keras.callbacks.ModelCheckpoint(NOW.strftime("%Y%m%d-%H%M%S") 
                                                  + 'best_loss.hdf5', 
                                                  monitor='val_acc', 
                                                  mode='max',
                                                  save_best_only=True)
    # option that display tensorboard
    # console >> tensorboard --logdir=~/your/path/logs
    tblogger = TrainValTensorBoard(log_dir='./logs',
                                   write_graph=True, 
                                   write_grads=True)
    
    ### training step
    hist = ImgNet.fit(x=xtrain, y=ytrain,
                      validation_data=(),
                      batch_size=BATCH_SIZE, 
                      epochs=EPOCHS, 
                      verbose=1, 
                      callbacks=[cb_check, tblogger])
    
    ### save history
    scipy.io.savemat(NOW.strftime("%Y%m%d-%H%M%S") 
                     + '_ImgNet_history.mat',
                     {'accu_tra':hist.history['acc'],
                      'accu_val':hist.history['val_acc'],
                      'loss_tra':hist.history['loss'],
                      'loss_val':hist.history['val_loss']})
    
    ### display
    plt.plot(hist.history['val_acc'])
    plt.plot(hist.history['acc'])

if __name__  == '__main__':
    main()
