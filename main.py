from collectors.cpuCollector import CpuCollector
from collectors.diskCollector import DiskCollector
from collectors.memoryCollector import MemoryCollector
from collectors.networkCollector import NetworkCollector
from influxDBConnection import InfluxDBConnection
import time

if __name__ == "__main__":
    influx_client = InfluxDBConnection()
    cpu = CpuCollector(influx_client)
    disk = DiskCollector(influx_client)
    memory = MemoryCollector(influx_client)
    network = NetworkCollector(influx_client)

    try:
        print("System metrics collection started...")
        while True:
            cpu.cpu_usage()
            cpu.cpu_times()
            cpu.cpu_frequency()
            cpu.cpu_stats()
            # cpu.cpu_temperature()
            cpu.cpu_load_average()
            # cpu.cpu_affinity()
            cpu.cpu_count()
            cpu.cpu_times_per_core()
            #
            disk.disk_usage()
            disk.disk_partitions()
            disk.disk_io_counters()

            memory.collect_memory_usage()
            memory.collect_swap_usage()
            memory.collect_performance_stats()

            # memory.collect_process_memory_usage()

            network.collect_network_io()
            network.collect_network_interfaces()

            network.collect_network_connections()
            network.collect_network_stats()
            network.collect_bandwidth_usage()

    except KeyboardInterrupt:
        print("Metrics collection stopped.")
    finally:
        influx_client.close()
