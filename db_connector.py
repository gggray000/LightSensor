import os
from datetime import datetime
import pytz
from influxdb_client import InfluxDBClient, Point

INFLUXDB_URL = os.environ.get("INFLUXDB_URL", "http://influxdb2:8086")
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
    time_with_tz = datetime.now(tz).isoformat()
    return time_with_tz

def write_to_influx(value):
    point = Point("light_data") \
        .field("value", value) \
        .time(get_time())
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

def get_data():
    query_api = client.query_api()
    query = '''
        from(bucket: "light_sensor")
        |> range(start: -10m)
        |> filter(fn: (r) => 
            r._measurement == "light_data" and 
            r._field == "value"
        )
        |> last()
        '''
    result = query_api.query(org=INFLUXDB_ORG, query=query)

    for table in result:
        for record in table.records:
            return {
                "value": record.get_value(),
                "time": record.get_time()
            }

    return {
        "value": None,
        "time": None
    }
