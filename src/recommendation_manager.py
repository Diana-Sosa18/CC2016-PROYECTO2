import sys
from dotenv import load_dotenv
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from db_connection import Neo4jApp

# Cargar variables del archivo .env
load_dotenv()

# Obtener valores del archivo .env
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

class RecommendationManager:
    def __init__(self, driver):
        self.driver = driver

    def get_recommendations(self, estilo, clima):
        query = """
        MATCH (o:Outfit)-[:PERTENECE_A]->(s:Style {nombre: $estilo}),
              (o)-[:ADEQUADO_PARA]->(c:Climate {Name: $clima})
        RETURN o.Name AS Name, o.ID_Image AS ID_Image, o.Upper AS Upper, 
               o.Lower AS Lower, o.Footwear AS Footwear, o.Accesory AS Accesory
        LIMIT 5
        """
        with self.driver.session() as session:
            result = session.run(query, {
                "estilo": estilo,
                "clima": clima
            })
            return [dict(row) for row in result]

    def close(self):
        if self.driver:
            self.driver.close()
