import unittest

from flask import Flask

app = Flask(__name__)


class TestWebHook(unittest.TestCase):

    def setUp(self):
        app.test_client()

    def test_webhook(self):
        pass

    def test_customer(self):
        pass
