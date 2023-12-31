# -*- coding: utf-8 -*-
"""neural_unb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/183Hb9Xk-ZnG4K9HgfRrRVVad3CkgBAHp
"""

from google.colab import files
uploaded = files.upload()

import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
import matplotlib.pyplot as plt
from keras.utils import pad_sequences

# Load the dataset
data = pd.read_csv('1unb_bin.csv')  # Assuming your dataset is in a CSV file

import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

# Split the dataset into features and labels
X = data.iloc[:, 2:].values  # Assuming the features start from the third column
y = data['Label'].values

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Encode labels using LabelEncoder
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Encode labels as one-hot vectors
num_classes = len(label_encoder.classes_)
y_train_encoded = to_categorical(y_train_encoded, num_classes)
y_test_encoded = to_categorical(y_test_encoded, num_classes)

from keras.callbacks import EarlyStopping

# Define the neural network model
model = Sequential()
model.add(Dense(16, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dense(32, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define early stopping criteria
early_stop = EarlyStopping(monitor='val_loss', patience=20, verbose=1)

# Train the model with early stopping
history = model.fit(X_train, y_train_encoded, epochs=400, batch_size=30, validation_data=(X_test, y_test_encoded), callbacks=[early_stop])

from sklearn.metrics import classification_report
import numpy as np

# Assuming you have the trained model stored in the variable 'model' and the test data stored in 'X_test' and 'y_test_encoded'

# Make predictions on the test data
y_pred_encoded = model.predict(X_test)

# Convert the predictions from one-hot encoded format to class labels
y_pred = np.argmax(y_pred_encoded, axis=1)

# Convert the true labels from one-hot encoded format to class labels
y_true = np.argmax(y_test_encoded, axis=1)

# Calculate precision, recall, and F1 score
report = classification_report(y_true, y_pred, digits=5)

print(report)

import matplotlib.pyplot as plt
import numpy as np

# Evaluate the model on test data
loss, accuracy = model.evaluate(X_test, y_test_encoded)
print("Test Loss: {:.5f}".format(loss))
print("Test Accuracy: {:.5f}".format(accuracy))

from sklearn.metrics import classification_report

# Assuming you have predictions for the test data in the variable 'y_pred_encoded'

# Convert the predictions from one-hot encoded format to class labels
y_pred = np.argmax(y_test_encoded, axis=1)

# Convert the true labels from one-hot encoded format to class labels
y_true = np.argmax(y_test_encoded, axis=1)

# Calculate precision, recall, and F1 score
report = classification_report(y_true, y_pred)

print(report)


# Plot the loss vs epoch graph
epochs = range(1, len(history.history['loss']) + 1)
train_loss = history.history['loss']
val_loss = history.history['val_loss']

plt.plot(epochs, train_loss, 'b-', label='Training Loss')
plt.plot(epochs, val_loss, 'r-', label='Validation Loss')
plt.title('Loss vs Epoch')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()