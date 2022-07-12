import pytest
import logging

from flask import template_rendered
from server import create_app

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app({"TESTING": True})
    _app.logger.setLevel(logging.CRITICAL)
    _app.testing = True
    yield _app


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
