import logging
import inspect

class ImprovedDebug(logging.Logger):
    """
    Improves debug level output.
    code from: http://www.karoltomala.com/blog/?p=720
    """	
    
    def debug(self, msg, *args, **kwargs):
        method = inspect.stack()[1][3]
        frm = inspect.stack()[1][0]
        if 'self' in frm.f_locals:
            clsname = frm.f_locals['self'].__class__.__name__
            method = clsname + '.' + method
        if not method.startswith('<'):
            method += '()'
        msg = ':'.join((method, str(frm.f_lineno), msg))
        self.__class__.__bases__[0].debug(self, msg, *args, **kwargs)

logging.setLoggerClass(ImprovedDebug)
getLogger = logging.getLogger

# Farseer-NMR logging configuration
farseer_log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "debug_format": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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