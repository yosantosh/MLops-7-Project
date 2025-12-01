import logging
from logging.handlers import RotatingFileHandler
from from_root import from_root     # it hept to get root directory 
from datetime import datetime 
import os


# constants for log configuration 
log_dir = 'logs'
log_file_naming_format = f"{datetime.now().strftime('%m_%d_%Y__%H')}.log"
max_log_file_size = 5*1024*1024          #5mb
backup_count = 3           # how many log files RotatingFileHandler can make when one log file filled with 5mb of data, then it will create new log file but cant make more than 3 files



# configure log file path
log_dir_path = os.path.join(from_root(),log_dir)
os.makedirs(log_dir_path,exist_ok=True)
log_file_path = os.path.join(log_dir_path,log_file_naming_format)


def configure_logger():
    "Logger func with RotatingFileHandler and console handler"

    # creating logger object
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    #define formatter
    format = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

    #file handler with rotation 
    file_handler = RotatingFileHandler(log_file_path,maxBytes=max_log_file_size, backupCount=backup_count)
    file_handler.setFormatter(format)
    file_handler.setLevel(logging.DEBUG)

    #console handler
    console = logging.StreamHandler()
    console.setFormatter(format)
    console.setLevel(logging.DEBUG)

    # adding handler into logger
    logger.addHandler(file_handler)
    logger.addHandler(console)



configure_logger()

# Reduce overly-verbose third-party loggers (e.g. pymongo heartbeats)
# Keep application logs at DEBUG but silence noisy libraries.
for _name in (
    "pymongo",
    "pymongo.topology",
    "pymongo.server_selection",
    "pymongo.connection",
    "pymongo.pool",
):
    logging.getLogger(_name).setLevel(logging.WARNING)




