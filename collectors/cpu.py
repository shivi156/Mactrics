import logging
import psutil
from datetime import datetime, timezone

from reactivex.operators import timestamp

from influxDBConnection import InfluxDBConnection
from config import OUTPUT_FILE, ERROR_FILE

class Cpu:
    def __init__(self, influx_client: InfluxDBConnection):
        self.influx_client = influx_client

    def cpu_usage(self):
        logging.basicConfig(level=logging.INFO, filename=OUTPUT_FILE, filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            timestamp = datetime.now(timezone.utc)
            # wonder if i can put the timestamp in the constructor and will it be accurate ?????

            self.influx_client.write_data('CPU_Metrics', 'CPU_Usage', cpu_usage, timestamp)

            # logger stuff here ...
            logging.info(f"Stored CPU usage: {cpu_usage}%")
            print(timestamp)
            print(f"Stored CPU usage: {cpu_usage}%")

        except Exception as e:
            logging.basicConfig(level=logging.ERROR, filename=ERROR_FILE, filemode="w",
                                format="%(asctime)s %(levelname)s %(message)s")
            logging.error(f"Error collecting / storing CPU usage: {e}")

    def cpu_times(self):
        try:
            user_cpu_time = psutil.cpu_times().user
            system_cpu_time = psutil.cpu_times().system
            idle_cpu_time = psutil.cpu_times().idle
            timestamp = datetime.now(timezone.utc)

            self.influx_client.write_data('CPU_Metrics', 'User_CPU_time', user_cpu_time, timestamp)
            self.influx_client.write_data('CPU_Metrics', 'System_CPU_time', system_cpu_time, timestamp)
            self.influx_client.write_data('CPU_Metrics', 'Idle_CPU_time', idle_cpu_time, timestamp)

            logging.info(f"Stored CPU user time: {user_cpu_time}%")
            logging.info(f"Stored CPU system time: {system_cpu_time}%")
            logging.info(f"Stored CPU idle time: {idle_cpu_time}%")
            print(f"Stored CPU usage: {user_cpu_time}%")
            print(f"Stored CPU usage: {system_cpu_time}%")
            print(f"Stored CPU usage: {idle_cpu_time}%")

        except Exception as e:
            # THIS ISNT CHANGING THE FILE LOCATION !!!!!!!
            logging.basicConfig(level=logging.ERROR, filename=ERROR_FILE, filemode="w",
                                format="%(asctime)s %(levelname)s %(message)s")
            logging.error(f"Error collecting / storing CPU times: {e}")



