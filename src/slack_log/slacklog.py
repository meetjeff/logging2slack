import logging
import requests
import json

class SlackLoggingHandler(logging.Handler):
    def __init__(self, webhook_url: str, logger_name: str, logger_icon: str):
        super().__init__()
        self.webhook_url = webhook_url
        self.logger_name = logger_name
        self.logger_icon = logger_icon

    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            "text": f"{log_entry}",
            "username": self.logger_name,
            "icon_emoji": self.logger_icon
        }
        requests.post(
            self.webhook_url, 
            data=json.dumps(payload), 
            headers={"Content-Type": "application/json"}
        )


class SlackLogger(logging.Logger):
    def __init__(
            self, 
            channel_list: dict, 
            logger_name: str='Service Log', 
            logger_icon: str=':middle_finger:'
        ):
        super().__init__("slack_logger", logging.DEBUG)
        self.channel_list = channel_list
        self.logger_name = logger_name
        self.logger_icon = logger_icon
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.get_channel()
    
    def get_channel(self):
        for level, channel in self.channel_list.items():
            self.set_handler(level, channel)

    def set_handler(self, level, channel):
        handler = SlackLoggingHandler(channel, self.logger_name, self.logger_icon)
        handler.setLevel(level)
        handler.setFormatter(self.formatter)
        self.addHandler(handler)