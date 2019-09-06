#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 12:20:00 2019

@author: jangho.lee.92
"""

import numpy as np


#---------------------------------------------------------------------------------------------------------
# -----  LOAD DATA  -----
# This data is for only 5% of total data due to overflowing memory problem
# 
# train_predictor, train_target, test_predictor, test_target
#---------------------------------------------------------------------------------------------------------

# Enter season
season='winter'

# Load training data
train_predictor=np.load('../data/seasonal_data/'+season+'_train_predictor.npy')
train_target=np.load('../data/seasonal_data/'+season+'_train_target.npy')
# Load test data
test_predictor=np.load('../data/seasonal_data/'+season+'_test_predictor.npy')
test_target=np.load('../data/seasonal_data/'+season+'_test_target.npy')



#---------------------------------------------------------------------------------------------------------
# ----- Create and Compile CNN Model -----
#---------------------------------------------------------------------------------------------------------

from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dropout, Reshape
import keras
from keras.utils import to_categorical

surr=5
window=5
channel=32
ker1= 5
ker2= 4
fil1= 80
fil2= 120
fil3= 150
mpl= 2
dr= 0.5
num_classes=2
class_weight = {0: 1.,
                1: 5.}

# Model
model=Sequential()
# 4 Conv Layer
model.add(Reshape((surr,window, channel), input_shape=(surr,window, channel)))
model.add(Conv2D(fil1, (mpl,mpl), activation='relu', padding = 'same', data_format='channels_last', input_shape=(surr,window, channel)))
model.add(Dropout(dr))
model.add(Conv2D(fil3, (mpl, mpl), activation='relu', padding = 'same'))
model.add(Conv2D(fil2, (mpl, mpl), activation='relu', padding = 'same'))
model.add(Conv2D(fil1, (mpl, mpl), activation='relu', padding = 'same'))
model.add(MaxPooling2D(pool_size=(mpl, mpl)))
model.add(Dropout(dr))
model.add(Conv2D(10, (1, 1), padding='valid'))
# Global Pooling and Dense
model.add(GlobalAveragePooling2D())
model.add(Dense(1, activation='sigmoid'))
print(model.summary())

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

callbacks_list = [keras.callbacks.ModelCheckpoint(\
        filepath='../CNN_models/'+season+'_2d32v/best_model.{epoch:02d}-{val_loss:.2f}.h5')]


#---------------------------------------------------------------------------------------------------------
# ----- FIT CNN Model -----
#---------------------------------------------------------------------------------------------------------
history=model.fit(train_predictor, train_target, batch_size=5000, epochs=50,\
                  callbacks=callbacks_list, class_weight=class_weight,\
                  validation_data=[test_predictor, test_target], verbose=1)

