import os, multiprocessing, sys
import logging as log
import logging.handlers as handlers
#import tensorflow as tf
import paho.mqtt.client as paho
import process # process.py

# tf can't be imported before multiprocessing occurs, otherwise you get errors
# https://www.tensorflow.org/api_docs/python/tf/config/list_physical_devices
#print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# https://kobkrit.com/using-allow-growth-memory-option-in-tensorflow-and-keras-dc8c8081bc96
# https://github.com/tensorflow/tensorflow/issues/33504
# https://www.tensorflow.org/api_docs/python/tf/config/experimental/set_memory_growth
#tf.config.experimental.set_memory_growth(tf.config.list_physical_devices('GPU') [0], True)  # allow GPU memory to grow dynamically

#print(tf.reduce_sum(tf.random.normal([1000, 1000])))

# turn off warnings about memory usage
# https://stackoverflow.com/questions/50304156/tensorflow-allocation-memory-allocation-of-38535168-exceeds-10-of-system-memor
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# yolov3-tiny runs about 10x faster than yolov3 on CPU?
yolo_model = "yolov3"
#yolo_model = "yolov3-tiny"

# define the labels to look for, 80 items in the yolov3 pretrained set, see .cfg file and the "classes" value
# https://github.com/amikelive/coco-labels/blob/master/coco-labels-2014_2017.txt
labels = ["person", "bicycle", "car", "motorbike", "bus", "truck"]
# reducing this and re-generating the .weights file doesn't seem to improve performance
# https://stackoverflow.com/questions/57898577/how-to-reduce-number-of-classes-in-yolov3-files

# mqtt setup
mqttclient = paho.Client()
mqttclient.connect("192.168.1.113", 1883)

p1 = multiprocessing.Process(target=process.run_process_monitor, args=("1", 20, mqttclient, labels, yolo_model, ))
#p2 = multiprocessing.Process(target=process.run_process_monitor, args=("2", 30, mqttclient, labels, yolo_model, ))

p1.start()
#p2.start()

# for debugging purposes
input("Press Enter to exit...\n")
p1.terminate()
