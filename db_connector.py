import os
from datetime import datetime

import pytz
from influxdb_client import InfluxDBClient, Point, WritePrecision

INFLUXDB_URL = os.environ.get("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG", "Dynamics e.V.")
INFLUXDB_BUCKET = os.environ.get("INFLUXDB_BUCKET", "light_sensor")

client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)

write_api = client.write_api()

def get_time():
    tz = pytz.timezone("Europe/Berlin")
    time_with_tz = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return time_with_tz

def write_to_influx(value):
    point = Point("light_data") \
        .field("value", value) \
        .time(get_time(), WritePrecision.NS)
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

def get_data():
    query_api = client.query_api()
    query = 'from(bucket:"light_sensor")\
    |> range(start: -10m)\
    |> filter(fn:(r) => r._measurement == "light_data") \
    |> limit (n:1)'
    result = query_api.query(org=INFLUXDB_ORG, query=query)
    return result
