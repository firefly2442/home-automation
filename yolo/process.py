import requests, sys, json, time, os, datetime, multiprocessing
import logging as log
import logging.handlers as handlers
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import tensorflow as tf
import paho.mqtt.client as paho
import common # common.py
from absl import flags
from absl.flags import FLAGS
import cv2
import numpy as np
sys.path.insert(0, "/yolo/yolov3-tf2/")
from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny
)
from yolov3_tf2.dataset import transform_images, load_tfrecord_dataset
from yolov3_tf2.utils import draw_outputs


def run_process_monitor(monitorid, fps, mqttclient, labels, yolo_model):
    logging = common.setupLogging(log, handlers, sys)

    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    for physical_device in physical_devices:
        tf.config.experimental.set_memory_growth(physical_device, True)
    
    logging.info("Num GPUs Available: " + str(len(physical_devices)))

    from urllib3.exceptions import InsecureRequestWarning
    # Suppress only the single warning from urllib3 about insecure requests
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    logging.info("Running monitor " + monitorid)
    
    # load yolov3 model
    # https://stackoverflow.com/questions/53295570/userwarning-no-training-configuration-found-in-save-file-the-model-was-not-c
    # anchors must be divisible by 32
    if (yolo_model == "yolov3"):
        yolo = YoloV3(classes=FLAGS.num_classes)
        FLAGS.weights = "/yolo/yolov3-tf2/checkpoints/yolov3.tf"
    elif (yolo_model == "yolov3-tiny"):
        yolo = YoloV3Tiny(classes=FLAGS.num_classes)
        FLAGS.weights = "/yolo/yolov3-tf2/checkpoints/yolov3-tiny.tf"
    
    yolo.load_weights(FLAGS.weights).expect_partial()

    class_names = [c.strip() for c in open(FLAGS.classes).readlines()]

    # while 1 is slightly faster than while True
    while 1:
        try:
            # https://zoneminder.readthedocs.io/en/latest/api.html
            monitor = requests.get("https://zoneminder:443/zm/api/events/index/MonitorId:"+monitorid+".json?sort=StartTime&direction=desc", verify=False)
            if (monitor.ok):
                data = monitor.json()
                continue_exec = True
                run_every_frames = 1
                frame_now = 1
                while (continue_exec):
                    event = requests.get("https://zoneminder:443/zm/api/events/"+str(data['events'][0]['Event']['Id'])+".json", verify=False)
                    if (event.ok):
                        event_data = event.json()
                        logging.info("Number frames to process: " + str(event_data['event']['Event']['Frames']))
                        if (event_data['event']['Event']['Next'] is not None):
                            continue_exec = False
                        filesystem_path = event_data['event']['Event']['FileSystemPath']
                        
                        for frame_num in range(1, int(event_data['event']['Event']['Frames'])):
                            start_time = datetime.datetime.now()
                            jpg_path = os.path.join(filesystem_path, str(frame_num).zfill(5) + "-capture.jpg")
                            if (os.path.isfile(jpg_path) and (frame_now == run_every_frames or (frame_num - frame_now) % run_every_frames == 0)):
                                # Understanding YOLO
                                # https://www.dlology.com/blog/gentle-guide-on-how-yolo-object-localization-works-with-keras-part-2/
                                # https://towardsdatascience.com/dive-really-deep-into-yolo-v3-a-beginners-guide-9e3d2666280e
                                # https://github.com/qqwweee/keras-yolo3
                                # https://github.com/zzh8829/yolov3-tf2

                                # see here for example: https://github.com/zzh8829/yolov3-tf2/blob/master/detect.py
                                logging.info(jpg_path)
                                FLAGS.image = jpg_path
                                if FLAGS.tfrecord:
                                    dataset = load_tfrecord_dataset(FLAGS.tfrecord, FLAGS.classes, FLAGS.size)
                                    dataset = dataset.shuffle(512)
                                    img_raw, _label = next(iter(dataset.take(1)))
                                else:
                                    img_raw = tf.image.decode_image(open(FLAGS.image, 'rb').read(), channels=3)

                                img = tf.expand_dims(img_raw, 0)
                                img = transform_images(img, FLAGS.size)

                                boxes, scores, classes, nums = yolo(img)

                                img = cv2.cvtColor(img_raw.numpy(), cv2.COLOR_RGB2BGR)
                                img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
                                FLAGS.output = '/testing/'+os.path.splitext(os.path.basename(jpg_path))[0]+'-bb.jpg'
                                cv2.imwrite(FLAGS.output, img)
                                for i in range(nums[0]):
                                    logging.info('\t{}, {}, {}'.format(class_names[int(classes[0][i])],
                                                                    np.array(scores[0][i]),
                                                                    np.array(boxes[0][i])))
                                    ret = mqttclient.publish("home-assistant/zoneminder/yolo/"+monitorid+"/", str(class_names[int(classes[0][i])]) + str(np.array(scores[0][i])))
                                    # TODO: error trapping on mqtt failure, check ret
                                skipped_frame = False
                                frame_now = 1
                            else:
                                skipped_frame = True
                                frame_now = frame_now + 1
                                
                            # delete the original file to save space
                            if os.path.exists(jpg_path):
                                os.remove(jpg_path)
                            if (not skipped_frame):
                                time_delta = (datetime.datetime.now() - start_time).total_seconds() * 1000 # milliseconds
                                logging.info("MS check: " + str(((run_every_frames/fps) * 1000)))
                                logging.info("Time delta: " + str(time_delta))
                                logging.info("Run every x frames: " + str(run_every_frames))
                                run_every_frames = round(round((time_delta/1000)*fps) * 1.1) # *1.1 so that we are slightly ahead
                                logging.info("New run every x frames: " + str(run_every_frames))
                                logging.info("Running at " + str(round(((1 / (time_delta/1000))/fps)*100, 2)) + " percent of FPS")
                    else:
                        time.sleep(1)
            else:
                logging.error(str(monitor))
                logging.error(monitor.json())
                            
                            

        except Exception as e:
            logging.error(str(e))
        
        time.sleep(5)
