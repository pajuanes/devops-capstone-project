"""
Unit Tests for error_handlers.py
"""
from unittest import TestCase
from unittest.mock import patch
from service import app
from service.models import DataValidationError
from service.common import status


class TestErrorHandlers(TestCase):
    """Test Error Handlers"""

    def setUp(self):
        self.client = app.test_client()
        app.logger.disabled = True

    def tearDown(self):
        app.logger.disabled = False

    # ------------------------------------------------------------------
    # DataValidationError -> 400
    # ------------------------------------------------------------------
    def test_request_validation_error(self):
        """DataValidationError debe retornar 400 Bad Request"""
        with app.test_request_context():
            from service.common.error_handlers import request_validation_error
            error = DataValidationError("invalid data")
            response, code = request_validation_error(error)
            data = response.get_json()

        self.assertEqual(code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["status"], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["error"], "Bad Request")
        self.assertIn("invalid data", data["message"])

    # ------------------------------------------------------------------
    # 400 Bad Request
    # ------------------------------------------------------------------
    def test_bad_request(self):
        """400 debe retornar JSON con error Bad Request"""
        with app.test_request_context():
            from service.common.error_handlers import bad_request
            response, code = bad_request(Exception("bad input"))
            data = response.get_json()

        self.assertEqual(code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["status"], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["error"], "Bad Request")
        self.assertIn("bad input", data["message"])

    # ------------------------------------------------------------------
    # 404 Not Found
    # ------------------------------------------------------------------
    def test_not_found(self):
        """404 debe retornar JSON con error Not Found"""
        with app.test_request_context():
            from service.common.error_handlers import not_found
            response, code = not_found(Exception("resource not found"))
            data = response.get_json()

        self.assertEqual(code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(data["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(data["error"], "Not Found")
        self.assertIn("resource not found", data["message"])

    # ------------------------------------------------------------------
    # 405 Method Not Allowed
    # ------------------------------------------------------------------
    def test_method_not_supported(self):
        """405 debe retornar JSON con error Method not Allowed"""
        # with app.test_request_context():
        from service.common.error_handlers import method_not_supported
        # response, code = method_not_supported(Exception("method not allowed"))

        # @app.errorhandler(405)

        @app.route("/test-405", methods=["GET"])
        def test_route():
            return "ok"

        # Hacemos POST a una ruta que solo permite GET → 405
        response = self.client.post("/test-405")

        print("Response from method_not_supported:", response)
        data = response.get_json()

        # self.assertEqual(code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data["status"], status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(data["error"], "Method not Allowed")
        # self.assertIn("method not allowed", data["message"])

    # ------------------------------------------------------------------
    # 415 Unsupported Media Type
    # ------------------------------------------------------------------
    def test_mediatype_not_supported(self):
        """415 debe retornar JSON con error Unsupported media type"""
        with app.test_request_context():
            from service.common.error_handlers import mediatype_not_supported
            response, code = mediatype_not_supported(Exception("unsupported media"))
            data = response.get_json()

        self.assertEqual(code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertEqual(data["status"], status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertEqual(data["error"], "Unsupported media type")
        self.assertIn("unsupported media", data["message"])

    # ------------------------------------------------------------------
    # 500 Internal Server Error
    # ------------------------------------------------------------------
    def test_internal_server_error(self):
        """500 debe retornar JSON con error Internal Server Error"""
        with app.test_request_context():
            from service.common.error_handlers import internal_server_error
            response, code = internal_server_error(Exception("something broke"))
            data = response.get_json()

        self.assertEqual(code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(data["status"], status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(data["error"], "Internal Server Error")
        self.assertIn("something broke", data["message"])
