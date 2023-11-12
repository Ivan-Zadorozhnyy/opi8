import pytest
import threading
from flask import Flask
from werkzeug.serving import make_server
from main import create_app, setup_database, seed_data


class TestE2ETests:
    driver = None

    @classmethod
    def setup_class(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        setup_database(cls.app)
        seed_data(cls.app)

        cls.server = make_server('localhost', 0, cls.app)
        cls.port = cls.server.server_port
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.start()

    @classmethod
    def teardown_class(cls):
        if cls.driver:
            cls.driver.quit()

        cls.server.shutdown()
        cls.server_thread.join()
        cls.app_context.pop()

    def test_api_reports(self):
        response = self.app.test_client().get('/api/reports')
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_index_route(self):

        response = self.app.test_client().get('/')
        assert response.status_code == 200

        assert "<title>API Endpoint Report</title>" in response.get_data(as_text=True)

        assert "<h1>API Endpoints</h1>" in response.get_data(as_text=True)
