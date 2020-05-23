#!/usr/bin/env python
from CO2Meter.CO2Meter import *
from datetime import date, datetime
import time

import csv
import codecs
import os.path as osp
import psycopg2

Meter = CO2Meter("/dev/co2")

sql = """INSERT INTO co2(co2, temp_c, humidity)
         VALUES(%s, %s, %s);"""
conn = None
vendor_id = None


try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postregs")
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print("connection error:")
    print(error)
    exit()
while True:
    try:
        measurement = {'co2': None, 'temperature': None, 'humidity': None}
        measurement.update(Meter.get_data())
        if measurement['co2']:
            cur.execute(sql, (measurement['co2'], measurement['temperature'], measurement['humidity']))
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    time.sleep(5)
if conn is not None:
    cur.close()
    conn.close()

