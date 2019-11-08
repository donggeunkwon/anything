# -*- coding: utf-8 -*-
"""ImageLoader.Loader

@author: Donggeun Kwon (donggeun.kwon@gmail.com)

Cryptographic Algorithm Lab.
Graduate School of Information Security, Korea University
"""

import numpy as np
import os
import pandas as pd
from tqdm import tqdm
import zipfile
from urllib.request import urlretrieve

import cv2


class Loader:
    def __init__(self, img_path=None):
        if img_path==None:
            self.PATH = './' 
            print('PATH="' + os.getcwd() + '"')
        else:
            self.PATH  = img_path.replace("\\", '/')
            self.PATH = self.PATH + '/' if self.PATH[-1]!='/' else self.PATH
        
        if (not os.path.isdir(self.PATH+'train/') and 
            not os.path.isdir(self.PATH+'val/')):
            if (not os.path.isdir(self.PATH+'tiny-imagenet-200/train/') and 
            not os.path.isdir(self.PATH+'tiny-imagenet-200/val/')):
                self.download_img()
            else:
                self.PATH = self.PATH + 'tiny-imagenet-200/'
                print('PATH="' + self.PATH + '"')
        else:
            print('./train/ exists')
        # image shape = 64 * 64 * 3
        self.NUM_CLASSES = 200
        self.NUM_CHANNELS = 3
        self.IMAGE_SIZE = 64
        self.IMAGE_ARR_SIZE = (self.IMAGE_SIZE **2) * self.NUM_CHANNELS
        
        self.TRAINING_IMAGES_DIR = self.PATH + 'train/'
        self.NUM_IMAGES_PER_CLASS = 500
        self.NUM_IMAGES = self.NUM_IMAGES_PER_CLASS * self.NUM_CLASSES
        
        self.VAL_IMAGES_DIR = self.PATH + 'val/'
        self.NUM_VAL_PER_CLASS = 50
        self.NUM_VAL_IMAGES = self.NUM_VAL_PER_CLASS * self.NUM_CLASSES
        
        self.IMG_CATEGORIES = np.asarray(os.listdir(self.TRAINING_IMAGES_DIR))
    
    def download_img(self):
        url = 'http://cs231n.stanford.edu/'
        file = 'tiny-imagenet-200.zip'
        try:
            zip_file = zipfile.ZipFile(self.PATH + '/' + file)
        except:
            with tqdm(unit='B', unit_scale=True, unit_divisor=1024, 
                  miniters=1, desc='Tiny-ImageNet-') as t:
                urlretrieve(url + file, self.PATH + file, reporthook=TqdmUpTo(t))
            zip_file = zipfile.ZipFile(self.PATH + '/' + file)
        print('extract ' + file, end=' ...')
        zip_file.extractall(self.PATH)
        zip_file.close()
        print(' end')
        self.PATH = self.PATH + "tiny-imagenet-200/"
    
    def load_train_img(self, image_dir=None):
        image_dir = self.TRAINING_IMAGES_DIR if image_dir==None else image_dir.replace("\\", '/')
        image_dir = image_dir + '/' if image_dir!=None and image_dir[-1]!='/' else image_dir
        
        images = np.ndarray(shape=(self.NUM_IMAGES, 
				   self.IMAGE_SIZE,
				   self.IMAGE_SIZE,
				   self.NUM_CHANNELS))
        labels = []
        imgdir = os.listdir(image_dir)
        image_index = 0
        
        print("Loading training images from ", image_dir)
        
        for i in tqdm(range(len(imgdir))):
            if os.path.isdir(image_dir + imgdir[i] + '/images/'):
                for image in os.listdir(image_dir + imgdir[i] + '/images/'):
                    image_file = os.path.join(image_dir,imgdir[i]+'/images/',image)
                    image_data = cv2.imread(image_file) 
                    if (image_data.shape==(self.IMAGE_SIZE, 
                                           self.IMAGE_SIZE, 
                                           self.NUM_CHANNELS)):
                        images[image_index, :] = np.reshape(image_data, [self.IMAGE_SIZE, 
																		 self.IMAGE_SIZE, 
																		 self.NUM_CHANNELS])
                        labels.append(str(imgdir[i]))
                        image_index += 1
                    else:
                        # print(image + ' failed ...')
                        pass
                    
        return (images[:image_index], np.asarray(labels)) 
    
    # val_images, val_labels = load_validation_images(VAL_IMAGES_DIR)
    def load_valid_img(self, testdir=None):
        testdir = self.VAL_IMAGES_DIR if testdir==None else testdir.replace("\\", '/')
        testdir = testdir + '/' if testdir!=None and testdir[-1]!='/' else testdir
        
        images = np.ndarray(shape=(self.NUM_VAL_IMAGES,
				   self.IMAGE_SIZE,
				   self.IMAGE_SIZE,
				   self.NUM_CHANNELS))
        image_index = 0
        labels = []
        val_images = os.listdir(testdir + '/images/')
        label_data = pd.read_csv(testdir + 'val_annotations.txt', 
                               sep='\t', header=None, 
                               names=['File', 'Class', 'X', 'Y', 'H', 'W'])
        label = label_data['Class'].values
        
        print("Loading validation images from ", testdir)
        
        for i in tqdm(range(len(val_images))):
            image_file = os.path.join(testdir, 'images/', val_images[i])
            image_data = cv2.imread(image_file) 
            
            if (image_data.shape==(self.IMAGE_SIZE, 
                                   self.IMAGE_SIZE, 
                                   self.NUM_CHANNELS)):
                images[image_index, :] = np.reshape(image_data, [self.IMAGE_SIZE, 
								 self.IMAGE_SIZE, 
								 self.NUM_CHANNELS])
                labels.append(str(label[i]))
                image_index += 1
            else:
                # print(image + ' failed ...')
                pass
        
        return (images[:image_index], np.asarray(labels))
    
    # label = onehot_encoding(label, IMG_CATEGORIES)
    def one_hot(self, labels, img_class=None):
        img_class = self.IMG_CATEGORIES if img_class==None else img_class
        label = []
        for i in range(len(labels)):
            label.append(np.where(img_class==labels[i])[0][0])
        
        return np.eye(self.NUM_CLASSES)[label]

# ProgressBar with tqdm
def TqdmUpTo(t):
    last_b = [0]
    def update_to(b=1, bsize=1, tsize=None):
        if tsize is not None:
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b
    return update_to
