import os
import csv


images = [] 


#append all he images in list
with open('./data/driving_log.csv') as csvfile: 
    reader = csv.reader(csvfile)
    next(reader, None)
    for line in reader:
        images.append(line)


from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

#split training and validation sample
train_samples, validation_samples = train_test_split(samples,test_size=0.15)


import cv2
import numpy as np
import sklearn
import matplotlib.pyplot as plt


def generator(images, batch_size=32):
    num_samples = len(images)
   
    while 1: 
        shuffle(images) 
        for offset in range(0, num_samples, batch_size):
            
            batch_samples = images[offset:offset+batch_size]

            images_aug = []
            angles_aug = []
            for batch_sample in batch_samples:
                #read left,right and center image and add correction in measurement
                    for i in range(0,3):
                        
                        name = './data/IMG/'+batch_sample[i].split('/')[-1]
                        center_image = cv2.cvtColor(cv2.imread(name), cv2.COLOR_BGR2RGB) 
                        center_angle = float(batch_sample[3]) 
                        images_aug.append(center_image)
                        
                        
                        if(i==0):
                            angles_aug.append(center_angle)
                        elif(i==1):
                            angles_aug.append(center_angle+0.2)
                        elif(i==2):
                            angles_aug.append(center_angle-0.2)
   
                        images_aug.append(cv2.flip(center_image,1))
                        if(i==0):
                            angles_aug.append(center_angle*-1)
                        elif(i==1):
                            angles_aug.append((center_angle+0.2)*-1)
                        elif(i==2):
                            angles_aug.append((center_angle-0.2)*-1)
  
                        
        
            X_train = np.array(images_aug)
            y_train = np.array(angles_aug)
            
            yield sklearn.utils.shuffle(X_train, y_train) 
            

train_generator = generator(train_samples, batch_size=32)
validation_generator = generator(validation_samples, batch_size=32)

from keras.models import Sequential
from keras.layers.core import Dense, Flatten, Activation, Dropout
from keras.layers.convolutional import Convolution2D
from keras.layers import Lambda, Cropping2D


#Nvidea model with some modification from mentor help discussion forum
model = Sequential()
model.add(Lambda(lambda x: (x / 255.0) - 0.5, input_shape=(160,320,3)))
model.add(Cropping2D(cropping=((70,25),(0,0))))           
model.add(Convolution2D(24,5,5,subsample=(2,2)))
model.add(Activation('elu'))
model.add(Convolution2D(36,5,5,subsample=(2,2)))
model.add(Activation('elu'))
model.add(Convolution2D(48,5,5,subsample=(2,2)))
model.add(Activation('elu'))
model.add(Convolution2D(64,3,3))
model.add(Activation('elu'))
model.add(Convolution2D(64,3,3))
model.add(Activation('elu'))
model.add(Flatten())
model.add(Dense(100))
model.add(Activation('elu'))
model.add(Dropout(0.25))
model.add(Dense(50))
model.add(Activation('elu'))
model.add(Dense(10))
model.add(Activation('elu'))
model.add(Dense(1)) 


model.compile(loss='mse',optimizer='adam')

model.fit_generator(train_generator, samples_per_epoch= len(train_samples), validation_data=validation_generator,   nb_val_samples=len(validation_samples), nb_epoch=5, verbose=1)

model.save('model.h5')

model.summary()
