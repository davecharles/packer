import unittest.mock

import pytest


def pytest_namespace():
    """Add mock to the pytest namespace"""
    return {'Mock': unittest.mock.Mock}
