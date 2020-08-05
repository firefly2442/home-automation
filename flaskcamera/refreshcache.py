import requests, time


while (True):
    try:
        # every so often, make a connection and load the page to keep the cache up-to-date
        # TODO: parameterize this, if we have more than one camera this will not work
        monitor = requests.get("http://localhost:5000/camera/sensor.outside_camera_mqtt_full")
        if (monitor.ok):
            pass
        else:
            print("Unable to connect")
        time.sleep(900) # 900 seconds is 15 minutes
    except Exception as e:
        print("Error: " + str(e))
        time.sleep(10)
