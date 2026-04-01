"""
Unit Tests for log_handlers.py
"""
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.common.log_handlers import init_logging


class TestLogHandlers(TestCase):
    """Test Log Handlers"""

    def test_init_logging_without_handlers(self):
        """init_logging sin handlers no ejecuta setFormatter"""
        with patch("logging.getLogger") as mock_get_logger:
            mock_gunicorn = MagicMock()
            mock_gunicorn.handlers = []
            mock_gunicorn.level = logging.DEBUG
            mock_get_logger.return_value = mock_gunicorn

            init_logging(app, "gunicorn.error")

            self.assertFalse(app.logger.propagate)
            self.assertEqual(app.logger.level, logging.DEBUG)

    def test_init_logging_with_handlers(self):
        """init_logging con handlers ejecuta setFormatter en cada uno"""
        mock_handler = MagicMock(spec=logging.StreamHandler)

        with patch("logging.getLogger") as mock_get_logger:
            mock_gunicorn = MagicMock()
            mock_gunicorn.handlers = [mock_handler]
            mock_gunicorn.level = logging.WARNING
            mock_get_logger.return_value = mock_gunicorn

            init_logging(app, "gunicorn.error")

            mock_handler.setFormatter.assert_called_once()
            formatter_arg = mock_handler.setFormatter.call_args[0][0]
            self.assertIsInstance(formatter_arg, logging.Formatter)
