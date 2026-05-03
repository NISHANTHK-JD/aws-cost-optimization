import unittest
from app.app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_returns_json(self):
        response = self.client.get("/")
        data = response.get_json()
        self.assertEqual(data["status"], "ok")

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")

if __name__ == "__main__":
    unittest.main()
