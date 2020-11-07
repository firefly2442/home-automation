import os, multiprocessing, time
import paho.mqtt.client as paho
from absl import app, flags
import process # process.py


flags.DEFINE_string('classes', '/yolo/yolov3-tf2/data/coco.names', 'path to classes file')
flags.DEFINE_string('weights', '/yolo/yolov3-tf2/checkpoints/yolov3.tf', 'path to weights file')
flags.DEFINE_boolean('tiny', False, 'yolov3 or yolov3-tiny')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_string('image', '', 'path to input image')
flags.DEFINE_string('output', '', 'path to output image')
flags.DEFINE_integer('num_classes', 80, 'number of classes in the model')

def main(_argv):
    # turn off warnings about memory usage
    # https://stackoverflow.com/questions/50304156/tensorflow-allocation-memory-allocation-of-38535168-exceeds-10-of-system-memor
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    # yolov3-tiny runs faster but accuracy is quite poor
    yolo_model = "yolov3"
    #yolo_model = "yolov3-tiny"

    # define the labels to look for, 80 items in the yolov3 pretrained set, see .cfg file and the "classes" value
    # https://github.com/amikelive/coco-labels/blob/master/coco-labels-2014_2017.txt
    #monitor_one_labels = ["person", "bicycle", "car", "motorbike", "bus", "truck"]
    #monitor_two_labels = ["person"]
    # reducing the labels and re-generating the .weights file doesn't seem to improve performance
    # https://stackoverflow.com/questions/57898577/how-to-reduce-number-of-classes-in-yolov3-files

    # mqtt setup
    mqttclient = paho.Client()
    mqttclient.connect("192.168.1.226", 1883)

    # we can't use pyinstrument on processes so this is for debugging manually
    # process.run_process_monitor("1", 20, mqttclient, ["person"], yolo_model)
    # process.run_process_monitor("2", 30, mqttclient, ["person"], yolo_model)

    procs = [None, None]

    while 1 is slightly faster than while True
    while 1:
        for i,proc in enumerate(procs):
            restart_it = False
            if proc is not None:
                proc.join(timeout=0)
                if not proc.is_alive():
                    restart_it = True
            else:
                restart_it = True

            # start up processing for true parallelism
            if restart_it:
                if i == 0:
                    p1 = multiprocessing.Process(target=process.run_process_monitor, args=("1", 20, mqttclient, ["person"], yolo_model, ))
                    p1.start()
                    procs[i] = p1
                elif i == 1:
                    p2 = multiprocessing.Process(target=process.run_process_monitor, args=("2", 30, mqttclient, ["person"], yolo_model, ))
                    p2.start()
                    procs[i] = p2
            else:
                time.sleep(5)


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
