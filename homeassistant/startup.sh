#!/bin/bash

# blocks until zoneminder is ready to prevent race condition with HA startup
python3 /check_zoneminder.py

/init
