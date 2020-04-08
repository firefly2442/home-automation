import requests, sys, json, time, os
import logging as log
import logging.handlers as handlers
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import tensorflow as tf
import detect # detect.py

from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 about insecure requests
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# https://www.tensorflow.org/api_docs/python/tf/config/list_physical_devices
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# https://kobkrit.com/using-allow-growth-memory-option-in-tensorflow-and-keras-dc8c8081bc96
# https://github.com/tensorflow/tensorflow/issues/33504
# https://www.tensorflow.org/api_docs/python/tf/config/experimental/set_memory_growth
# tf.config.experimental.set_memory_growth(tf.config.list_physical_devices('GPU') [0], True)  # allow GPU memory to grow dynamically

# turn off warnings about memory usage
# https://stackoverflow.com/questions/50304156/tensorflow-allocation-memory-allocation-of-38535168-exceeds-10-of-system-memor
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# TODO: switch to Python logging to stdout

# load yolov3 model
# https://stackoverflow.com/questions/53295570/userwarning-no-training-configuration-found-in-save-file-the-model-was-not-c
model = load_model('/yolo/model.h5', compile=False)

# define the labels to look for
# https://github.com/amikelive/coco-labels/blob/master/coco-labels-2014_2017.txt
labels = ["person", "bicycle", "car", "motorbike", "bus", "truck"]

while True:
    time.sleep(5)