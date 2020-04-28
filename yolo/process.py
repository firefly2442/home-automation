import requests, sys, json, time, os, datetime, multiprocessing
import logging as log
import logging.handlers as handlers
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import tensorflow as tf
import paho.mqtt.client as paho
import detect # detect.py
import common # common.py


def run_process_monitor(monitorid, fps, mqttclient, labels, yolo_model):
    logging = common.setupLogging(log, handlers, sys)

    logging.info("Num GPUs Available: " + str(len(tf.config.list_physical_devices('GPU'))))

    from urllib3.exceptions import InsecureRequestWarning
    # Suppress only the single warning from urllib3 about insecure requests
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    logging.info("Running monitor " + monitorid)
    
    # load yolov3 model
    # https://stackoverflow.com/questions/53295570/userwarning-no-training-configuration-found-in-save-file-the-model-was-not-c
    if (yolo_model == "yolov3"):
        model = load_model('/yolo/model.h5', compile=False)
        # yolov3 anchors
        anchors = [[116,90, 156,198, 373,326], [30,61, 62,45, 59,119], [10,13, 16,30, 33,23]]
        # define the expected input shape for the model, see .cfg file for width and heigh in the [net] section, must be divisible by 32
        input_w, input_h = 608, 608
    elif (yolo_model == "yolov3-tiny"):
        model = load_model('/yolo/model-tiny.h5', compile=False)
        # yolov3-tiny anchors
        # TODO: is there something wrong with the .cfg files? these anchors don't work
        # anchors = [[135,169, 344,319], [37,58, 81,82], [10,14,  23,27]]
        # https://github.com/pjreddie/darknet/issues/568
        anchors = [[116,90, 156,198, 373,326], [30,61, 62,45, 59,119], [10,13, 16,30, 33,23]]
        # define the expected input shape for the model, see .cfg file for width and height in the [net] section, must be divisible by 32
        input_w, input_h = 416, 416

    while True:
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

                                logging.info(jpg_path)
                                # load and prepare image
                                image, image_w, image_h = detect.load_image_pixels(jpg_path, (input_w, input_h))
                                # make prediction
                                # https://keras.io/models/model/
                                yhat = model.predict(image, verbose=0, use_multiprocessing=True)
                                # define the probability threshold for detected objects
                                class_threshold = 0.6
                                boxes = list()
                                for i in range(len(yhat)):
                                    # decode the output of the network
                                    boxes += detect.decode_netout(yhat[i][0], anchors[i], class_threshold, input_h, input_w)
                                # correct the sizes of the bounding boxes for the shape of the image
                                detect.correct_yolo_boxes(boxes, image_h, image_w, input_h, input_w)
                                # suppress non-maximal boxes
                                boxes = detect.do_nms(boxes, 0.5)
                                # get the details of the detected objects
                                v_boxes, v_labels, v_scores = detect.get_boxes(boxes, labels, class_threshold)
                                # summarize what we found
                                for i in range(len(v_boxes)):
                                    logging.info(str(v_labels[i]) + " - " + str(v_scores[i]))
                                    ret = mqttclient.publish("home-assistant/zoneminder/yolo/"+monitorid+"/", str(v_labels[i]) + str(v_scores[i]))
                                    # TODO: error trapping on mqtt failure, check ret
                                # draw what we found
                                detect.draw_boxes(jpg_path, v_boxes, v_labels, v_scores)
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
                    time.sleep(1)
            else:
                logging.error(str(monitor))
                logging.error(monitor.json())
                            
                            

        except Exception as e:
            logging.error(str(e))
        
        time.sleep(5)
