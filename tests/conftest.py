import pytest
from webserver import app
from apps.chat_bot import routes

@pytest.fixture
def app():
    app.blueprint(routes.chat_bot_blueprint)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
