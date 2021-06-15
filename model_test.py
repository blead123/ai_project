import tensorflow as tf
from tensorflow.keras.models import load_model

detect_model = load_model(filepath='./5000_test_model.h5')
detect_model.summary()