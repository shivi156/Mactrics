import configparser

# This reads the config file
config = configparser.ConfigParser()
config.read('config.ini')

# This configures InfluxDB
URL = config['InfluxDB']['URL']
TOKEN = config['InfluxDB']['Token']
ORG = config['InfluxDB']['ORG']
BUCKET = config['InfluxDB']['BUCKET']

# This configures logging
OUTPUT_FILE = config['LOGGING']['OUTPUT_FILE']
