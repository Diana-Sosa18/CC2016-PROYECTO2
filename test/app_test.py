'''
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_recommend_missing_data(client):
    response = client.post('/recommend', json={})
    assert response.status_code == 400
    assert "Faltan datos" in response.json.get("error", "")

def test_recommend_no_results(client):
    data = {
        "user": "usuario_que_no_existe",
        "estilo": "estilo_falso",
        "clima": "clima_falso",
        "ocasion": "ocasion_falsa"
    }
    response = client.post('/recommend', json=data)
    assert response.status_code == 404
    assert "No se encontraron recomendaciones" in response.json.get("message", "")
'''
