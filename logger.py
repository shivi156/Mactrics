import logging
from config import OUTPUT_FILE, ERROR_FILE

class Logger:

    def standardOutput(self):
        logging.basicConfig(level=logging.INFO, filename=OUTPUT_FILE, filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")

    def errorOutput(self):
        logging.basicConfig(level=logging.ERROR, filename=OUTPUT_FILE, filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")