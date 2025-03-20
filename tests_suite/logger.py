import logging
from pythonjsonlogger import jsonlogger
import inspect
import datetime


class JSONLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler('reports/logs/test_logs.json')
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_test_step(self, status, msg, test_name, error=None):
        # Extract the calling test function name
        log_data = {
            "testname": test_name,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "status": status,
            "error": str(error) if error else None,
            "msg": msg
        }
        self.logger.info(log_data)
