import psutil
from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point, WritePrecision
from cpu import Cpu

# InfluxDB Configuration
influx_url = "http://localhost:8086"
influx_token = "0ouh1VuC_XbadQTRhdbxZlGQPMxl9fOo40ovyx1MeBy4rCLc0L8Et7nn3Ol9_aJlgMQbUsQ20db2-LKsV810wA=="
influx_org = "University of Chester"
influx_bucket = "performance_metrics"

# Initialise the InfluxDB client
client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)

# Testing CPU usage collection and storing it in InfluxDB
def collect_and_store_cpu_usage():
    # Collect CPU usage (percentage)
    cpu_usage = psutil.cpu_percent(interval=1)

    # Create a test Point for the CPU usage data
    point = Point("cpu_usage") \
        .tag("host", "local_machine") \
        .field("usage", cpu_usage) \
        .time(datetime.now(timezone.utc), WritePrecision.MS)

    write_api = client.write_api()
    write_api.write(bucket=influx_bucket, record=point)

    print(f"Stored CPU usage: {cpu_usage}%")

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
