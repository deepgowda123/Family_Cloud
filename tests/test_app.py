import sys
import os

# Add parent dir to import app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

def test_home_page():
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

