# -*- coding: utf-8 -*-
"""main_ml_yo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z2uRy05uaNmRDNMt9dmjRks6PCmKCeDd
"""

!pip install tensorflow==1.13.0
!pip install keras==2.2.4

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

import pandas as pd
import numpy as np

data = pd.read_csv("main_yo.csv")
data = data.replace([np.inf, -np.inf], np.nan)

data_set = []
data_for_word = []
letters = []
tags = []
for i,letter in enumerate(data['letter']):
  if str(letter) == 'nan':
    data_set.append(data_for_word)
    data_for_word = []
  else:
    data_for_word.append((letter, data['target'][i]))
    letters.append(letter)
    tags.append(data['target'][i])

letter = set(letters)
new_letters = [i for i in letter]
new_letters.sort()
print(new_letters)

max_len = 20
letter2idx = {w: i + 1 for i, w in enumerate(new_letters)}

print(letter2idx)

from keras.preprocessing.sequence import pad_sequences
X = [[letter2idx[l[0]] for l in s] for s in data_set]
X = pad_sequences(maxlen=max_len, sequences=X, padding="post", value=0)

y = [[l[1] for l in s] for s in data_set]

y = pad_sequences(maxlen=max_len, sequences=y, padding="post", value=0)

print(len(X), len(y))

pip install np_utils

from sklearn.model_selection import train_test_split
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.1)

pip install git+https://www.github.com/keras-team/keras-contrib.git

from keras.models import Model, Input
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional
from keras_contrib.layers import CRF

input = Input(shape=(max_len,))
model = Embedding(input_dim=35, output_dim=10,
                  input_length=max_len, mask_zero=True)(input)  
model = Bidirectional(LSTM(units=50, return_sequences=True,
                           recurrent_dropout=0.1))(model)  
model = TimeDistributed(Dense(50, activation="relu"))(model) 
crf = CRF(2)  
out = crf(model)

model = Model(input, out)

model.compile(optimizer="rmsprop", loss=crf.loss_function, metrics=[crf.accuracy])
model.summary()

print(X_tr[:10])
print(y_tr[:10])

history = model.fit(X_tr, np.array(y_tr), batch_size=32, epochs=5,
                    validation_split=0.1, verbose=1)