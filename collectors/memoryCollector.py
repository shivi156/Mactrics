import psutil
import logging
from datetime import datetime, timezone
from influxDBConnection import InfluxDBConnection
from config import OUTPUT_FILE

class MemoryCollector:
    def __init__(self, influx_client: InfluxDBConnection):
        self.influx_client = influx_client
        logging.basicConfig(level=logging.INFO,
                            filename=OUTPUT_FILE,
                            filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")

    def collect_and_store(self, measurement: str, fields: dict, tags: dict = None):
        try:
            timestamp = datetime.now(timezone.utc)
            self.influx_client.write_data(measurement, fields, timestamp, tags or {})
            logging.info(f"Stored {measurement}: {tags or {}} -> {fields}")
            print(f"Stored {measurement}: {tags or {}} -> {fields}")
        except Exception as e:
            logging.error(f"Error writing {measurement} to InfluxDB: {e}")


    def collect_memory_usage(self):
        mem = psutil.virtual_memory()
        fields = {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'free': mem.free,
            'percent': mem.percent
        }
        self.collect_and_store("memory_usage", fields)

    def collect_swap_usage(self):
        swap = psutil.swap_memory()
        fields = {
            'total': swap.total,
            'used': swap.used,
            'free': swap.free,
            'percent': swap.percent,
            'swap_in': swap.sin,
            'swap_out': swap.sout
        }
        self.collect_and_store("swap_usage", fields)

    def collect_performance_stats(self):
        cpu_percents = psutil.cpu_percent(percpu=True)
        ram_percent = psutil.virtual_memory().percent
        fields = {
            'ram_percent': ram_percent
        }

        for i, cpu in enumerate(cpu_percents):
            fields[f'cpu_core_{i}_percent'] = cpu
        self.collect_and_store("performance_stats", fields)
