from neo4j import GraphDatabase, basic_auth
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Obtener valores del archivo .env
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

class Neo4jApp:

    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))
            # Probar conexión
            with self.driver.session() as session:
                result = session.run("RETURN 1")
                if result.single()[0] == 1:
                    print("✅ Conexión exitosa a la base de datos Neo4j.")
        except Exception as e:
            print("❌ Error al conectar a Neo4j:")
            print(e)

    def close(self):
        self.driver.close()

    def ejecutar_consulta(self, consulta):
        with self.driver.session() as session:
            resultado = session.run(consulta)
            for registro in resultado:
                print(registro)

if __name__ == "__main__":
    app = Neo4jApp(URI, USER, PASSWORD)
    app.ejecutar_consulta("MATCH (n) RETURN n LIMIT 5")
    app.close()
