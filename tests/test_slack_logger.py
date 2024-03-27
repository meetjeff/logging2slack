import unittest
import logging
from unittest.mock import patch

from logging2slack import SlackLogger, SlackLoggingHandler

class TestLoggingUtils(unittest.TestCase):
    def setUp(self):
        self.slack_url = "http://example.com/webhook"
        self.channel_list = {
            "INFO":self.slack_url,
            "WARN":self.slack_url
        }
        self.logger_name = "test_logger"
        self.logger_icon = ":test_icon:"

    @patch('logging2slack.slack_logger.requests.post')
    def test_emit(self, mock_post):
        handler = SlackLoggingHandler(
            self.slack_url, 
            self.logger_name, 
            self.logger_icon
        )
        handler.setLevel(logging.INFO)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )

        log_record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg="Test log message",
            args=(),
            exc_info=None
        )

        handler.emit(log_record)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], self.slack_url)
        self.assertTrue("Test log message" in kwargs["data"])

    def test_logger(self):
        logger = SlackLogger(
            self.channel_list, 
            self.logger_name, 
            self.logger_icon
        )
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "slack_logger")
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertTrue(
            any(isinstance(h, SlackLoggingHandler) for h in logger.handlers)
        )