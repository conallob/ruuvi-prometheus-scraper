#!/usr/bin/python3

import time
import pprint
import signal
import sys
from prometheus_client import Gauge
from prometheus_client import start_http_server
from ruuvitag_sensor.ruuvi import RuuviTagSensor

beacons = {
    '12:34:56:78:90:AB': {
        'name': 'master_bedroom',
        'last_update': 0.0,
        'sensor_data': {},
    },
}

temp_gauge = Gauge('ruuvi_temperature_c', 'Temperature in Celsius', ['location'])
humidity_gauge = Gauge('ruuvi_humidity_percent', 'Humidity %', ['location'])
pressure_gauge = Gauge('ruuvi_pressure_hpa', 'Air pressure hPa', ['location'])
battery_gauge = Gauge('ruuvi_battery_v', 'Battery V', ['location'])

def handle_data(data):
    [mac, sensor_data] = data
    beacon = beacons[mac]
    beacon['last_update'] = time.time()
    beacon['sensor_data'] = sensor_data
    location = beacon['name']
    temp_gauge.labels(location).set(sensor_data['temperature'])
    humidity_gauge.labels(location).set(sensor_data['humidity'] / 100.0)
    pressure_gauge.labels(location).set(sensor_data['pressure'])
    battery_gauge.labels(location).set(sensor_data['battery'] / 1000.0)

def sigint_handler(signal, frame):
    print("Collected data:")
    pprint.pprint(beacons)
    sys.exit(130)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    print("Starting HTTP server for Prometheus scraping")
    start_http_server(9521)

    print("Reading data from Ruuvi tags")
    RuuviTagSensor.get_datas(handle_data, beacons.keys())
