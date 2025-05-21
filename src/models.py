import re
import bcrypt
from datetime import datetime
from db_connection import Neo4jApp, URI, USER, PASSWORD

class UserManager:
    def __init__(self):
        self.app = Neo4jApp(URI, USER, PASSWORD)

    def _execute_query_with_result(self, query, parameters=None):
        with self.app.driver.session() as session:
            result = session.run(query, parameters or {})
            return result.data()

    def user_exists(self, username):
        query = "MATCH (u:User {username: $username}) RETURN u"
        result = self._execute_query_with_result(query, {"username": username})
        return len(result) > 0

    def _is_password_strong(self, password):
        """
        Verifica que la contraseña cumpla las restricciones correspondientes. 
        """
        return (
            len(password) >= 6 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'\d', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        )

    def register_user(self, username, password):
        if not self._is_password_strong(password):
            return False, (
                "La contraseña debe tener al menos 6 caracteres, "
                "una letra mayúscula, una letra minúscula, un número y un símbolo especial."
            )

        if self.user_exists(username):
            return False, "El usuario ya existe"

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = """
        CREATE (u:User {
            username: $username,
            password: $password,
            registration_date: $registration_date
        })
        """
        parameters = {
            "username": username,
            "password": hashed_password,
            "registration_date": current_date
        }
        with self.app.driver.session() as session:
            session.run(query, parameters)
        return True, "Usuario registrado con éxito"

    def login(self, username, password):
        query = "MATCH (u:User {username: $username}) RETURN u.password AS stored_password"
        result = self._execute_query_with_result(query, {"username": username})

        if not result:
            return False  # Usuario no encontrado

        stored_password = result[0]['stored_password']
        return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))

    def close(self):
        self.app.close()
