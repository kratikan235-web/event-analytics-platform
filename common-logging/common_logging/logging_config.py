import logging
import logging.config
import os


def setup_logging(service_name: str):

    log_level = os.getenv("LOG_LEVEL", "INFO")

    os.makedirs("logs", exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "standard": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            }
        },

        "handlers": {

            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": log_level
            },

            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": f"logs/{service_name}.log",
                "maxBytes": 5 * 1024 * 1024,
                "backupCount": 5,
                "formatter": "standard",
                "level": log_level
            }

        },

        "root": {
            "handlers": ["console", "file"],
            "level": log_level
        }
    }

    logging.config.dictConfig(logging_config)