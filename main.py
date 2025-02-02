import psutil
import time
import logging
from datetime import datetime, timezone
# from influxdb_client import InfluxDBClient, Point, WritePrecision
from cpu import Cpu
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB Configuration
influx_url = "http://localhost:8086"
influx_token = "0ouh1VuC_XbadQTRhdbxZlGQPMxl9fOo40ovyx1MeBy4rCLc0L8Et7nn3Ol9_aJlgMQbUsQ20db2-LKsV810wA=="
influx_org = "University of Chester"
influx_bucket = "performance_metrics"

# Initialise the InfluxDB client
client = influxdb_client.InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Testing CPU usage collection and storing it in InfluxDB
def collect_and_store_cpu_usage():
    # Collect CPU usage (percentage)
    cpu_usage = psutil.cpu_percent(interval=0.1)

    point = influxdb_client.Point("CPU-metrics").field("CPU_usage", cpu_usage).time(datetime.now(timezone.utc), WritePrecision.MS)
    write_api.write(bucket=influx_bucket, org=influx_org, record=point)

    # time.sleep(0.01)  # separate points by 1 second
    # print(f"Stored CPU usage: {cpu_usage}%")

    query_api = client.query_api()
    query = 'from(bucket:"test")\
    |> range(start: -10m)\
    |> filter(fn:(r) => r._measurement == "CPU-metrics")\
    |> filter(fn:(r) => r._field == "CPU_usage")'

    result = query_api.query(org=influx_org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))

    print(results)

if __name__ == "__main__":
    import time
    try:
        while True:
            collect_and_store_cpu_usage()
            time.sleep(1)  # Sleep for a second before collecting the next data
    except KeyboardInterrupt:
        print("Terminating the program.")
    finally:
        client.close()
