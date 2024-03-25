import logging
import os
from logging.handlers import TimedRotatingFileHandler


def create_log_folder(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

def register_logger(log_dir,log_file,level:logging = logging.DEBUG):
    create_log_folder(log_dir)
    
    log_file = os.path.join(log_dir, log_file)
    
    handler = TimedRotatingFileHandler(
        filename=log_file,
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger('appLogger')
    logger.addHandler(handler)
    logger.setLevel(level)  # Setting the log level as required
