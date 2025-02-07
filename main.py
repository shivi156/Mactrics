import psutil

from collectors.cpu import Cpu
from influxDBConnection import InfluxDBConnection

if __name__ == "__main__":
    influx_client = InfluxDBConnection()
    cpu = Cpu(influx_client)

    try:
        print("System metrics collection started...")
        while True:
            cpu.cpu_usage()
            cpu.cpu_times()
    except KeyboardInterrupt:
        print("Metrics collection stopped.")
    finally:
        influx_client.close()
