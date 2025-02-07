from dataclasses import field
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from config import URL, TOKEN, ORG, BUCKET

class InfluxDBConnection:
    '''
    Initialising the InfluxDB client
    '''
    def __init__(self):
        self.client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def write_data(self, measurement: str, field_key: str, value: float, timestamp):
        point = (influxdb_client.Point(measurement).field(field_key, value), timestamp)
        self.write_api.write(bucket=BUCKET, org=ORG, record=point)

    def query_data(self, measurement: str, field_key: str, time_range: str = "-2d"):
        query = f"""
            'from(bucket:"{BUCKET}")\
            |> range(start: {time_range})\
            |> filter(fn:(r) => r._measurement == "{measurement}")\
            |> filter(fn:(r) => r._field == "{field_key}")'
        """
        return self.query_api.query(org=ORG, query=query)

    def close(self):
        self.client.close()
