#!/usr/bin/python3

import time
import pprint
import signal
import sys
from prometheus_client import Gauge
from prometheus_client import start_http_server
from ruuvitag_sensor.ruuvi import RuuviTagSensor

beacons = {
    'F8:7F:12:D4:1F:E5': {
        'name': 'landing',
        'last_update': 0.0,
        'sensor_data': {},
    },
    'FA:5A:4A:CF:1C:29': {
        'name': 'sitting_room',
        'last_update': 0.0,
        'sensor_data': {},
    },
    'D2:34:FE:E2:5E:12': {
        'name': 'hall',
        'last_update': 0.0,
        'sensor_data': {},
    },
    'C7:E0:C1:DA:93:E7': {
        'name': 'reuben',
        'last_update': 0.0,
        'sensor_data': {},
    },
    'D0:78:21:66:46:3E': {
        'name': 'workshop',
        'last_update': 0.0,
        'sensor_data': {},
    },  
}

temp_gauge = Gauge('ruuvi_temperature_celsius', 'Temperature in Celsius', ['location'])
humidity_gauge = Gauge('ruuvi_humidity_percent', 'Humidity %', ['location'])
pressure_gauge = Gauge('ruuvi_pressure_hectopascals', 'Air pressure hPa', ['location'])
battery_gauge = Gauge('ruuvi_battery_volts', 'Battery V', ['location'])

def handle_data(data):
    [mac, sensor_data] = data
    beacons[mac]['last_update'] = time.time()
    beacons[mac]['sensor_data'] = sensor_data
    location = beacons[mac]['name']
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
    while True:
      RuuviTagSensor.get_datas(handle_data, beacons.keys())
      time.sleep(60)
