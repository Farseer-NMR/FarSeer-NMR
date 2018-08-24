import logging
import logging.config

# Farseer-NMR logging configuration
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

logging.config.dictConfig(farseer_log_config)
getLogger = logging.getLogger

if __name__ == "__main__":
    
    loggy = logging.getLogger(__name__)
    loggy.debug('llala')
    loggy.info('lele')
