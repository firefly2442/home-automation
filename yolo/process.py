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
        FLAGS.tiny = False
    elif (yolo_model == "yolov3-tiny"):
        yolo = YoloV3Tiny(classes=FLAGS.num_classes)
        FLAGS.weights = "/yolo/yolov3-tf2/checkpoints/yolov3-tiny.tf"
        FLAGS.tiny = True
    
    yolo.load_weights(FLAGS.weights).expect_partial()

    class_names = [c.strip() for c in open(FLAGS.classes).readlines()]

    # while 1 is slightly faster than while True
    while 1:
        try:
            # clear out the session so we don't have memory leaks
            tf.keras.backend.clear_session()
            # https://zoneminder.readthedocs.io/en/latest/api.html
            monitor_status = requests.get("https://zoneminder:443/zm/api/monitors.json", verify=False)
            if (monitor_status.ok):
                status = monitor_status.json()
                if (status['monitors'][int(monitorid)-1]['Monitor_Status']['Status'] == "Connected"):
                    monitor = requests.get("https://zoneminder:443/zm/api/events/index/MonitorId:"+monitorid+".json?sort=StartTime&direction=desc", verify=False)
                    if (monitor.ok):
                        data = monitor.json()
                        continue_exec = True
                        run_every_frames = 1
                        frame_now = 1
                        start_frame_at = 1
                        while (continue_exec):
                            event = requests.get("https://zoneminder:443/zm/api/events/"+str(data['events'][0]['Event']['Id'])+".json", verify=False)
                            time.sleep(0.5)
                            if (event.ok):
                                event_data = event.json()
                                logging.info("Number frames to process: " + str(event_data['event']['Event']['Frames']))
                                if (event_data['event']['Event']['Frames'] is not None):
                                    if (event_data['event']['Event']['Next'] is not None):
                                        continue_exec = False
                                    filesystem_path = event_data['event']['Event']['FileSystemPath']
                                    
                                    for frame_num in range(start_frame_at, int(event_data['event']['Event']['Frames'])):
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
                                            logging.info("Monitor " + monitorid + " running on frame: " + str(frame_num))
                                            FLAGS.image = jpg_path
                                            img_raw = tf.image.decode_image(open(FLAGS.image, 'rb').read(), channels=3)

                                            img = tf.expand_dims(img_raw, 0)
                                            img = transform_images(img, FLAGS.size)

                                            boxes, scores, classes, nums = yolo(img)
                                            # convert from EagerTensor objects to numpy arrays so that we can manipulate them
                                            boxes = boxes.numpy()
                                            scores = scores.numpy()
                                            classes = classes.numpy()
                                            nums = nums.numpy()

                                            i = 0
                                            while i < int(nums[0]):
                                                # filter out labels we're not interested in
                                                if (class_names[int(classes[0][i])] in labels and scores[0][i] > 0.7):
                                                    logging.info('\t{}, {}, {}'.format(class_names[int(classes[0][i])],
                                                                                    np.array(scores[0][i]),
                                                                                    np.array(boxes[0][i])))
                                                    # you have to use /config/www/ for Discord
                                                    # https://community.home-assistant.io/t/discord-image-notification/125735/13
                                                    # https://github.com/home-assistant/core/issues/26560
                                                    # get access to images served up from homeassistant via:
                                                    # http://192.168.1.113:8123/local/zoneminder/events/1/2020-06-07/3488/05328-capture.jpg
                                                    zm_path = jpg_path.replace("/var/cache/", "/config/www/")
                                                    # don't pass JSON with single quotes, otherwise it won't work
                                                    mqttclient.publish("home-assistant/zoneminder/yolo/"+monitorid+"/", "{\"label\": \"" + str(class_names[int(classes[0][i])]) + "\", \"img_path\": \"" + zm_path + "\", \"timestamp\": \"" + event_data['event']['Event']['StartTime'] + "\"}")
                                                    #logging.info("Writing to MQTT: " + "{\"label\": \"" + str(class_names[int(classes[0][i])]) + "\", \"img_path\": \"" + zm_path + "\", \"timestamp\": \"" + event_data['event']['Event']['StartTime'] + "\"}")
                                                else:
                                                    #logging.info("Removing item from image: " + str(class_names[int(classes[0][i])]) + " " + str(np.array(boxes[0][i])) + " " + str(np.array(scores[0][i])))
                                                    # clear out the arrays of stuff we don't care about so they don't get bounding boxes drawn
                                                    boxes = np.delete(boxes, i, axis=1) # 3D
                                                    scores = np.delete(scores, i, axis=1) # 2D
                                                    classes = np.delete(classes, i, axis=1) # 2D
                                                    nums[0] = int(nums[0]) - 1 # 1D
                                                    i = i - 1 # we're in-place removing items from arrays so we have to continue with the same index next go around
                                                i = i + 1
                                            if (nums[0] is not None and nums[0] != 0):
                                                img = cv2.cvtColor(img_raw.numpy(), cv2.COLOR_RGB2BGR)
                                                # TODO: parameterize coloring, put in PR upstream
                                                #logging.info("Writing image to disk: " + str(classes) + " " + str(boxes) + " " + str(scores))
                                                img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
                                                # overwrite image
                                                cv2.imwrite(jpg_path, img)
                                            # send an empty mqtt message so that home assistant doesn't show stale data into the future
                                            mqttclient.publish("home-assistant/zoneminder/yolo/"+monitorid+"/", "{\"label\": \"\", \"img_path\": \"\", \"timestamp\": \"\"}")
                                            skipped_frame = False
                                            frame_now = 1
                                        else:
                                            skipped_frame = True
                                            frame_now = frame_now + 1
                                            
                                        if (not skipped_frame):
                                            logging.info("Running monitor " + monitorid)
                                            time_delta = (datetime.datetime.now() - start_time).total_seconds() * 1000 # milliseconds
                                            #logging.info("MS check: " + str(((run_every_frames/fps) * 1000)))
                                            #logging.info("Time delta: " + str(time_delta))
                                            #logging.info("Run every x frames: " + str(run_every_frames))
                                            run_every_frames = round(round((time_delta/1000)*fps) * 1.1) # *1.1 so that we are slightly ahead
                                            logging.info("New run every x frames: " + str(run_every_frames))
                                    start_frame_at = int(event_data['event']['Event']['Frames'])
                            else:
                                time.sleep(1)
                    else:
                        logging.error(str(monitor))
                        logging.error(monitor.json())
                        time.sleep(1)
                else:
                    time.sleep(5) # monitor is not running in zoneminder, wait a bit
            else:
                logging.error(str(monitor_status))
                logging.error(monitor_status.json())
                time.sleep(1)

        except Exception as e:
            logging.error(str(e))
            time.sleep(1)