import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from recommendation_manager import RecommendationManager
from db_connection import URI, USER, PASSWORD
from neo4j import GraphDatabase

@pytest.fixture(scope="module")
def recommendation_manager():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    manager = RecommendationManager(driver)
    yield manager
    manager.close()

def test_get_outfit_recommendations(recommendation_manager):
    resultados = recommendation_manager.get_recommendations(
        estilo="Vintage",
        clima="Templado"
    )
    assert isinstance(resultados, list)
    assert all("Name" in r and "ID_Image" in r for r in resultados)

def test_get_recommendations_no_match(recommendation_manager):
    results = recommendation_manager.get_recommendations(
    estilo="estilo_falso", clima="clima_falso"
    )
    assert isinstance(results, list)
    assert len(results) == 0