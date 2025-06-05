import logging
import psutil
from datetime import datetime, timezone
from influxDBConnection import InfluxDBConnection
from config import OUTPUT_FILE

class CpuCollector:
    def __init__(self, influx_client: InfluxDBConnection):
        self.influx_client = influx_client
        logging.basicConfig(level=logging.INFO,
                            filename=OUTPUT_FILE,
                            filemode='w',
                            format='%(asctime)s %(levelname)s %(message)s')

    def collect_and_store(self, fields: dict, measurement: str, log_msg: str):
        timestamp = datetime.now(timezone.utc)
        self.influx_client.write_data(measurement, fields, timestamp)
        logging.info(log_msg.format(fields=fields))
        print(log_msg.format(fields=fields))

    def cpu_usage(self):
        try:
            cpu_usage = psutil.cpu_percent()
            self.collect_and_store(
                {'cpu_usage' : cpu_usage},
                'cpu_usage',
                'Stored CPU usage: {fields}'
            )
        except Exception as e:
            logging.error(f'Error collecting / storing CPU usage: {e}')

    def cpu_times(self):
        try:
            times = psutil.cpu_times()
            fields = {
                'user_cpu_time': times.user,
                'system_cpu_time': times.system,
                'idle_cpu_time': times.idle
            }
            self.collect_and_store(fields,
                                   'cpu_times',
                                   'Stored CPU times: {fields}')
        except Exception as e:
            logging.error(f'Error collecting / storing CPU times: {e}')

    def cpu_frequency(self):
        try:
            freq = psutil.cpu_freq()
            fields = {
                'current_frequency': freq.current,
                'min_frequency': freq.min,
                'max_frequency': freq.max
            }
            self.collect_and_store(fields,
                                   'cpu_frequency',
                                   'Stored CPU frequency: {fields}')
        except Exception as e:
            logging.error(f'Error collecting/storing CPU frequency: {e}')

    def cpu_stats(self):
        try:
            stats = psutil.cpu_stats()
            fields = {
                'context_switches': stats.ctx_switches,
                'interrupts': stats.interrupts,
                'soft_interrupts': stats.soft_interrupts
            }
            self.collect_and_store(fields,
                                   'cpu_stats',
                                   'Stored CPU stats: {fields}')
        except Exception as e:
            logging.error(f'Error collecting/storing CPU stats: {e}')

    def cpu_load_average(self):
        try:
            load1, load5, load15 = psutil.getloadavg()
            fields = {
                'load_1_min': load1,
                'load_5_min': load5,
                'load_15_min': load15
            }
            self.collect_and_store(fields,
                                   'cpu_load_average',
                                   'Stored CPU load average: {fields}')
        except Exception as e:
            logging.error(f"Error collecting/storing CPU load average: {e}")

    # THIS IS ONLY FOR LINUX LEARN THROUGH TESTING SO MENTION IT!!
    # def cpu_temperature(self):
    #     try:
    #         temps = psutil.sensors_temperatures()
    #         fields = {}
    #         for name, entries in temps.items():
    #             for entry in entries:
    #                 label = entry.label or 'temp'
    #                 fields[f'{name}_{label}'] = entry.current
    #
    #         if fields:
    #             self.collect_and_store(fields,
    #                                    'cpu_temperatures',
    #                                    'Stored CPU temperatures: {fields}')
    #         else:
    #             logging.info('No CPU temperature data available.')
    #     except Exception as e:
    #         logging.error(f'Error collecting/storing CPU temperatures: {e}')

    # Also unsupported on macOS
    # def cpu_affinity(self):
    #     try:
    #         affinity = psutil.Process().cpu_affinity()
    #         self.collect_and_store({'cpu_affinity_count': len(affinity)},
    #                                 'cpu_affinity',
    #                                 'Stored CPU affinity: {fields}')
    #     except Exception as e:
    #         logging.error(f'Error collecting/storing CPU affinity: {e}')

    def cpu_count(self):
        try:
            fields = {
                'logical_cpu_cores': psutil.cpu_count(logical=True),
                'physical_cpu_cores': psutil.cpu_count(logical=False)
            }
            self.collect_and_store(fields,
                                   'cpu_count',
                                   'Stored CPU core counts: {fields}')
        except Exception as e:
            logging.error(f'Error collecting/storing CPU core counts: {e}')

    def cpu_times_per_core(self):
        try:
            cores = psutil.cpu_times(percpu=True)
            fields = {}

            for i, times in enumerate(cores):
                fields.update({
                    f'core_{i}_user': times.user,
                    f'core_{i}_system': times.system,
                    f'core_{i}_idle': times.idle,
                    f'core_{i}_nice': getattr(times, 'nice', 0.0),
                    f'core_{i}_iowait': getattr(times, 'iowait', 0.0),
                    f'core_{i}_steal': getattr(times, 'steal', 0.0)
                })

            self.collect_and_store(fields,
                                   'cpu_times_per_core',
                                   'Stored per-core CPU times: {fields}')
        except Exception as e:
            logging.error(f'Error collecting/storing per-core CPU times: {e}')
