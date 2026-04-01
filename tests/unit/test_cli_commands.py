"""
CLI Command Extensions for Flask
"""
import os
from unittest import TestCase
from unittest.mock import patch, MagicMock
from service import app
from click.testing import CliRunner
from service.common.cli_commands import db_create


class TestFlaskCLI(TestCase):
    """Test Flask CLI Commands"""

    def setUp(self):
        # self.runner = CliRunner()
        self.runner = app.test_cli_runner()

    @patch("service.common.cli_commands.db", autospec=True)
    def test_db_create_ok(self, mock_db):
        """Prueba para db_create utilizando db.drop_all, db.create_all y db.session.commit"""
        mock_db.drop_all.return_value = None
        mock_db.create_all.return_value = None
        mock_db.session.commit.return_value = None

        # Invoca el comando CLI "db-create"
        print("Invocando el comando db_create...")
        # result = self.runner.invoke(db_create)
        result = self.runner.invoke(args=["db-create"])

        self.assertEqual(result.exit_code, 0)  

        # Verifica que drop_all fue llamado
        try:
            mock_db.drop_all.assert_called_once()
        except AssertionError as e:
            print("Error: drop_all no fue llamado correctamente.")
            raise e
        
        # Verifica que create_all fue llamado
        try:
            mock_db.create_all.assert_called_once()
        except AssertionError as e:
            print("Error: create_all no fue llamado correctamente.")
            raise e

        # Verifica que session.commit fue llamado
        try:
            mock_db.session.commit.assert_called_once()
        except AssertionError as e:
            print("Error: session.commit no fue llamado correctamente.")
            raise e

        # Verifica que el comando se ejecutó correctamente
        self.assertIn("Base de datos creada exitosamente", result.output)

    # Prueba para simular un error en db.drop_all
    @patch("service.common.cli_commands.db", autospec=True)
    def test_db_create_drop_all_fails(self, mock_db):
        mock_db.drop_all.side_effect = Exception("fallo en drop_all")

        result = self.runner.invoke(args=["db-create"])

        self.assertNotEqual(result.exit_code, 0)
        mock_db.drop_all.assert_called_once()
