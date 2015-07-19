#!/usr/bin/env python

import os
import glob
import time
import datetime
import MySQLdb as mdb

# Speichern der Temperatur in der Datenbank
def log_temperature(temp):
    con = mdb.connect('localhost', 'root', 'ostfalia', 'WeatherDB');
    cur = con.cursor()
    cur.execute("INSERT INTO `TB_Weather`(StationID, SensorID, MessWert) VALUES(1,1,%s)",(temp))
    con.commit()
    con.close()
    print "log_temperature durchlaufen"

# Oeffnen der Sensor-Datei und Auslesen der Werte
def get_temp(devicefile):
    try:
        fileobj = open(devicefile,'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        return None

    status = lines[0][-4:-1]

    if status=="YES":
        print status
        tempstr= lines[1][-6:-1]
        tempvalue=float(tempstr)/1000
        print tempvalue
        return tempvalue
    else:
        print "There was an error."
        return None


def main():

    # Suche nach dem Device, welches mit 28 startet
    # Alle ds-Sensoren fangen mit 28 an
    devicelist = glob.glob('/sys/bus/w1/devices/28*')
    if devicelist=='':
        return None
    # Wenn Sensor gefunden, haenge w1_slave an,
    #  um zur Temperatur-Datei zu gelangen
    else:
        w1devicefile = devicelist[0] + '/w1_slave'

    temperature = get_temp(w1devicefile)

    # Wenn kein Ergebnis, erneute Temp-Abfrage
    if temperature != None:
        print "temperature="+str(temperature)
    else:
        temperature = get_temp(w1devicefile)
        print "temperature="+str(temperature)
    log_temperature(temperature)

if __name__=="__main__":
    main()

