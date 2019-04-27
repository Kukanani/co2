#!/usr/bin/env python
from CO2Meter.CO2Meter import *
from datetime import date, datetime
import time

import csv
import codecs
import os.path as osp


FILENAME = "test.csv"
ENCODING = 'utf-8'
LOGDIR = "logs"


Meter = CO2Meter("/dev/hidraw0")
while True:
    start_day = date.today()
    fn = osp.join(LOGDIR, 'co2_{}.csv'.format(date.today().isoformat()))
    if osp.exists(fn):
        mode = "a"
    else:
        mode = "w"
    print(start_day)
    with open(fn, mode, encoding=ENCODING, buffering=1) as f:
        writer = csv.writer(f)
        if mode == "w":
            writer.writerow(['timestamp', 'co2', 'temperature', 'humidity'])
        measurement = {'co2': 0, 'temperature': 0, 'humidity': 0}
        while date.today() == start_day:
            measurement.update(Meter.get_data())
            if measurement['co2'] != 0:
                row = [datetime.now().replace(microsecond=0).isoformat(), measurement['co2'], measurement['temperature'], measurement['humidity']]
                print(row)
                writer.writerow(row)
                time.sleep(5)