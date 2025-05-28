import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from recommendation_manager import RecommendationManager
import pytest
from db_connection import URI, USER, PASSWORD


@pytest.fixture(scope="module")
def rec_manager():
    manager = RecommendationManager(URI, USER, PASSWORD)
    yield manager
    manager.close()

def test_get_recommendations_no_params(rec_manager):
    # Pasamos parámetros vacíos o no existentes para verificar manejo
    results = rec_manager.get_recommendations("usuario_que_no_existe", "estilo_falso", "clima_falso", "ocasion_falsa")
    assert isinstance(results, list)
    assert len(results) == 0

def test_get_outfit_recommendations(recommendation_manager):
    """
    Devuelve al menos un outfit adecuado al estilo y clima seleccionados.
    """
    resultados = recommendation_manager.get_recommendations(
        estilo="Vintage",
        clima="Templado"
    )
    assert len(resultados) > 0, "❌ No se devolvieron outfits"
    for r in resultados:
        assert "Name" in r and "ID_Image" in r


def test_get_outfit_recommendations_no_match(recommendation_manager):
    """
    No debe devolver nada si el estilo o clima no existen.
    """
    resultados = recommendation_manager.get_recommendations(
        estilo="Futurista",
        clima="Tormenta ácida"
    )
    assert resultados == [], "❌ Devolvió resultados cuando no debería"

