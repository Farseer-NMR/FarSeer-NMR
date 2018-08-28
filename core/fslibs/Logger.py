import logging
import logging.config

class FarseerLogger:
    """
    Farseer-NMR logger configuration
    """
    farseer_log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "debug_format": {
                "format": "%(asctime)s - %(levelname)s - %(filename)s:%(name)s:%(funcName)s:%(lineno)d - %(message)s"
            },
            "info_format": {}
        },
        
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "info_format",
                "stream": "ext://sys.stdout"
            },
            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "info_format",
                "filename": "farseernmr.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            },
            "debug_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "debug_format",
                "filename": "debug.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            }
        },
        
        "loggers": {},
        
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "info_file_handler", "debug_file_handler"]
        }
    }
    
    
    
    def __init__(self, name, new_dir=''):
        
        if new_dir:
            self.farseer_log_config["handlers"]["info_file_handler"]["filename"] = "{}/farseernmr.log".format(new_dir)
            self.farseer_log_config["handlers"]["debug_file_handler"]["filename"] = "{}/debug.log".format(new_dir)
        
        self.name = name
        #self.setup_log()
    
    def setup_log(self):
        
        logging.config.dictConfig(self.farseer_log_config)
        return logging.getLogger(self.name)

if __name__ == "__main__":
    
    loggy = FarseerLogger(__name__, new_dir='/home/joao/Programming/Farseer_testing').setup_log()
    #logger = loggy.setup_log()
    print(loggy)
    loggy.info('hahah')
    loggy.debug('hehe')
    
    log2 = FarseerLogger(__name__)
    print(log2.farseer_log_config["handlers"])
