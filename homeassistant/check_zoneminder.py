import requests, time, sys

while (True):
    try:
        # constantly ping zoneminder until it's ready
        # pass our certificate authority file that has been updated after running update-ca-certificates
        monitor = requests.get("https://192.168.1.113:8443/zm/api/host/getVersion.json", verify="/etc/ssl/certs/ca-certificates.crt")
        if (monitor.ok):
            print("Zoneminder is up", flush=True) # flush to stdout immediately
            sys.exit(0)
        else:
            print("Unable to connect to Zoneminder", flush=True)
        time.sleep(3)
    except Exception as e:
        print("Error: " + str(e), flush=True)
        time.sleep(3)