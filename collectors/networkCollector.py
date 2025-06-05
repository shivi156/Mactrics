import psutil
import logging
from influxDBConnection import InfluxDBConnection
from datetime import datetime, timezone
from config import OUTPUT_FILE

class NetworkCollector:
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

    def collect_network_io(self):
        try:
            io = psutil.net_io_counters()
            fields = {
                'bytes_sent': io.bytes_sent,
                'bytes_recv': io.bytes_recv,
                'packets_sent': io.packets_sent,
                'packets_recv': io.packets_recv,
                'errin': io.errin,
                'errout': io.errout,
                'dropin': io.dropin,
                'dropout': io.dropout
            }
            self.collect_and_store("network_io", fields)
        except Exception as e:
            logging.error(f"Error collecting network I/O: {e}")

    def collect_network_interfaces(self):
        try:
            interfaces = psutil.net_if_addrs()
            for iface, addrs in interfaces.items():
                for addr in addrs:
                    fields = {
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    }
                    tags = {'interface': iface, 'family': str(addr.family)}
                    self.collect_and_store("network_interface", fields, tags)
        except Exception as e:
            logging.error(f"Error collecting network interfaces: {e}")

    def collect_network_connections(self):
        try:
            for conn in psutil.net_connections(kind='inet'):
                try:
                    fields = {
                        'fd': conn.fd,
                        'family': conn.family,
                        'type': conn.type,
                        'laddr': str(conn.laddr),
                        'raddr': str(conn.raddr),
                        'status': conn.status
                    }
                    tags = {'pid': str(conn.pid) if conn.pid else 'N/A'}
                    self.collect_and_store("network_connection", fields, tags)
                except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
                    logging.debug(f"Skipping connection due to: {e}")
                except Exception as e:
                    logging.warning(f"Unexpected error with connection: {e}")
        except Exception as e:
            logging.error(f"Error listing network connections: {e}")

    def collect_network_stats(self):
        try:
            stats = psutil.net_if_stats()
            for iface, stat in stats.items():
                fields = {
                    'isup': stat.isup,
                    'duplex': stat.duplex,
                    'speed': stat.speed,
                    'mtu': stat.mtu
                }
                tags = {'interface': iface}
                self.collect_and_store("network_stats", fields, tags)
        except Exception as e:
            logging.error(f"Error collecting network stats: {e}")

    def collect_bandwidth_usage(self):
        try:
            stats = psutil.net_if_stats()
            for iface, stat in stats.items():
                fields = {
                    'max_speed': stat.speed,
                    'duplex_mode': stat.duplex
                }
                tags = {'interface': iface}
                self.collect_and_store("network_bandwidth", fields, tags)
        except Exception as e:
            logging.error(f"Error collecting bandwidth usage: {e}")
