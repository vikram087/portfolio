import os
import unittest

os.environ["TESTING"] = "true"

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Vikram Penumarti</title>" in html
        assert "portfolio" in html.lower() or "about" in html.lower()

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        post_data = {
            "name": "Test User",
            "email": "test@example.com",
            "content": "This is a test post",
        }
        response = self.client.post("/api/timeline_post", data=post_data)
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json["name"] == "Test User"
        assert json["email"] == "test@example.com"
        assert json["content"] == "This is a test post"

        response = self.client.get("/api/timeline_post")
        json = response.get_json()
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "Test User"

        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "timeline" in html.lower()

    def test_malformed_timeline_post(self):
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "missing name, email, or content" in html

        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "missing name, email, or content" in html

        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm John!",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
