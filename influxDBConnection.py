import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from config import URL, TOKEN, ORG, BUCKET

class InfluxDBConnection:

    def __init__(self):
        self.client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def write_data(self, measurement: str, fields: dict, timestamp, tags: dict = None):
        point = influxdb_client.Point(measurement).time(timestamp)

        if tags:
            for tag_key, tag_value in tags.items():
                point = point.tag(tag_key, str(tag_value))

        for field_key, value in fields.items():
            point = point.field(field_key, value)

        self.write_api.write(bucket=BUCKET, org=ORG, record=point)

    def close(self):
        self.client.close()
