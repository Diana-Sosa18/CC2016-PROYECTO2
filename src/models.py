from neo4j_conexion import Neo4jApp, URI, USER, PASSWORD
from datetime import datetime

class UserManager:
    def __init__(self):
        self.app = Neo4jApp(URI, USER, PASSWORD)
    
    def _execute_query_with_result(self, query):
       
        with self.app.driver.session() as session:
            result = session.run(query)
            return result.data()
    
    def user_exists(self, username):
        query = f"MATCH (u:User {{username: '{username}'}}) RETURN u"
        result = self._execute_query_with_result(query)
        return len(result) > 0
    
    def register_user(self, username, password):
        if self.user_exists(username):
            return False, "El usuario ya existe"
        
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = f"""
        CREATE (u:User {{
            username: '{username}',
            password: '{password}',
            registration_date: '{current_date}'
        }})
        """
        with self.app.driver.session() as session:
            session.run(query)
        return True, "Usuario registrado con exito"
    
    def login(self, username, password):
        query = f"""
        MATCH (u:User {{username: '{username}', password: '{password}'}})
        RETURN u
        """
        result = self._execute_query_with_result(query)
        return len(result) > 0
    
    def close(self):
        self.app.close()