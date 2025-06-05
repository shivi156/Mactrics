import psutil
import logging
from influxDBConnection import InfluxDBConnection
from datetime import datetime, timezone
from config import OUTPUT_FILE

class DiskCollector:
    def __init__(self, influx_client: InfluxDBConnection):
        self.influx_client = influx_client
        logging.basicConfig(level=logging.INFO,
                            filename=OUTPUT_FILE,
                            filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")

    def collect_and_store(self, measurement: str, fields: dict, tags: dict):
        timestamp = datetime.now(timezone.utc)
        try:
            self.influx_client.write_data(measurement, fields, timestamp, tags)
            message = f"Stored {measurement}: {tags} -> {fields}"
            logging.info(message)
            print(message)
        except Exception as e:
            logging.error(f"Error writing {measurement} data to InfluxDB: {e}")

    def disk_usage(self):
        for partition in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                fields = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
                tags = {
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype
                }
                self.collect_and_store("disk_usage", fields, tags)
            except PermissionError:
                logging.warning(f"Permission denied: {partition.mountpoint}")
            except Exception as e:
                logging.error(f"Error collecting usage for {partition.mountpoint}: {e}")

    def disk_partitions(self):
        try:
            for partition in psutil.disk_partitions(all=False):
                fields = {'opts': partition.opts}
                tags = {
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype
                }
                self.collect_and_store("disk_partitions", fields, tags)
        except Exception as e:
            logging.error(f"Error collecting disk partitions: {e}")

    def disk_io_counters(self):
        try:
            io_stats = psutil.disk_io_counters(perdisk=True)
            for device, stats in io_stats.items():
                fields = {
                    'read_count': stats.read_count,
                    'write_count': stats.write_count,
                    'read_bytes': stats.read_bytes,
                    'write_bytes': stats.write_bytes,
                    'read_time': stats.read_time,
                    'write_time': stats.write_time
                }
                tags = {'device': device}
                self.collect_and_store("disk_io_counters", fields, tags)
        except Exception as e:
            logging.error(f"Error collecting disk IO counters: {e}")
