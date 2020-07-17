import requests, json, re, os, imageio, base64, io, sys
from skimage.transform import rescale
from skimage.io import imread
from pygifsicle import optimize # https://github.com/LucaCappelletti94/pygifsicle
import numpy as np
import logging.handlers as handlers
import logging as log
from flask import Flask, render_template
import config # config.py
 
app = Flask(__name__)

logging = log.getLogger('flask')
logging.setLevel(log.DEBUG)
logHandler = log.StreamHandler()
logHandler.setLevel(log.DEBUG)
logHandler.setFormatter(log.Formatter("{%(pathname)s:%(lineno)d} %(asctime)s - %(levelname)s - %(message)s", '%m/%d/%Y %I:%M:%S %p'))
logging.addHandler(logHandler)

# https://developers.home-assistant.io/docs/api/rest/
# https://www.tutorialspoint.com/flask/index.htm

# curl -X GET \
#   -H "Authorization: Bearer secret" \
#   -H "Content-Type: application/json" \
#   http://192.168.1.113:8123/api/history/period?filter_entity_id=sensor.outside_camera_mqtt_full > test.json

def writeGIF(towrite, gif_images, clearimage=False):
    # /config/www/zoneminder/events/1/2020-07-01/7357/11001-capture.jpg
    # http://192.168.1.113:8123/local/zoneminder/events/1/2020-07-01/7357/11001-capture.jpg
    # https://192.168.1.113:8443/zm/index.php?view=event&eid=8061
    dt = re.search(r"^\d{4}-\d{2}-\d{2}", towrite['timestamp']).group()
    tm = re.search(r"\d{2}:\d{2}:\d{2}$", towrite['timestamp']).group()
    event_number = re.search(r"\d{4}-\d{2}-\d{2}\/(\d+)\/", towrite['img_path']).group(1)
    gif_name = towrite['img_path'].replace(".jpg", ".gif").replace("/", "_")
    # use cached GIF file if possible, lost on docker restart
    if (not os.path.isfile(gif_name)):
        # https://stackoverflow.com/questions/62530258/encoding-gif-to-base64-without-writing-to-disk-python
        # https://www.tutorialexample.com/understand-imageio-mimwrite-with-examples-for-beginners-imageio-tutorial/
        imageio.mimwrite(gif_name, gif_images, 'GIF', subrectangles=True, fps=1)
        # https://imageio.readthedocs.io/en/stable/examples.html#optimizing-a-gif-using-pygifsicle
        # optimize the GIF and reduce size
        optimize(gif_name)
    detect_base64 = 'data:image/gif;base64,{}'.format(base64.b64encode(open(gif_name, 'rb').read()).decode())
    if (clearimage):
        # delete the potential "partial" so it can be regenerated next time
        os.remove(gif_name)
    return(dt, tm, detect_base64, event_number)
                                

# e.g.: http://localhost:5000/camera/sensor.outside_camera_mqtt_full
@app.route('/camera/<camerasensor>')
def query_camera(camerasensor):
    try:
        logging.info(camerasensor)
        headers = {"Authorization": "Bearer " + config.homeassistant_token}
        params = {"filter_entity_id": camerasensor}
        # https://developers.home-assistant.io/docs/api/rest/#get-apihistoryperiodtimestamp
        monitor = requests.get("http://192.168.1.113:8123/api/history/period", headers=headers, params=params, verify=False)
        if monitor.ok:
            data = monitor.json()[0] # data is wrapped in an extra array thus the [0]
            templated_events = []
            gif_images = []
            prev = None
            state = None
            cleaned_data = []
            for event in data:
                if (event['state'] and event['state'] != "unknown" and event['state'] != "{\"label\": \"\", \"img_path\": \"\", \"timestamp\": \"\"}"):
                    #logging.info("adding: " + str(event['state']))
                    cleaned_data.append(event)
            for k,event in enumerate(cleaned_data):
                if (event['state']):
                    try:
                        state = json.loads(event['state'])
                    except ValueError:
                        pass # ignore other events for manual testing
                    if (state['img_path']):
                        # load in the already rescaled image so we don't have massive GIFs
                        state['img_path'] = state['img_path'].replace("-capture.jpg", "-capture_scaled.jpg")
                        if (state['img_path'] != "" and os.path.isfile(state['img_path'])):
                            #logging.info(state['img_path'])
                            if (prev is not None and state['timestamp'] != prev['timestamp']):
                                dt, tm, detect_base64, event_number = writeGIF(prev, gif_images)
                                templated_events.append({"date": dt, "time": tm, "base64": detect_base64, "eventnumber": event_number})
                                gif_images = []

                            gif_images.append(imread(state['img_path'], as_gray=False))
                            prev = state
                            logging.info("Processed " + str(k) + " of " + str(len(cleaned_data)))

            # kinda hacky but we need to make sure to write out whatever we have for the last event
            if (state):
                dt, tm, detect_base64, event_number = writeGIF(state, gif_images, clearimage=True)
                templated_events.append({"date": dt, "time": tm, "base64": detect_base64, "eventnumber": event_number})

            return render_template('index.html', events = templated_events)
        else:
            logging.error("Unable to connect to home assistant REST API")

    except Exception as e:
        logging.exception(str(e))
        return "Error: " + str(e)

    return "Something broke, check the code in app.py"

 
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
