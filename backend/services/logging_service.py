import logging


class LoggingService:
    def __init__(self):
        self.logger = logging.getLogger("ai-resume-tailoring-engine")

    def log_info(self, msg: str):
        self.logger.info(msg)

    def log_error(self, msg: str):
        self.logger.error(msg)

    def log_debug(self, msg: str):
        self.logger.debug(msg)
