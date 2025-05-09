from neo4j_conexion import Neo4jApp, URI, USER, PASSWORD
from datetime import datetime

class UserManager:
    def __init__(self):
        self.app = Neo4jApp(URI, USER, PASSWORD)
        self.current_user = None
    
    def _execute_query_with_result(self, query):
        try:
            with self.app.driver.session() as session:
                result = session.run(query)
                return result.data()
        except Exception as e:
            print(f"🔴 Error en consulta: {str(e)}")
            return None
    
    def _execute_write_query(self, query):
        try:
            with self.app.driver.session() as session:
                session.run(query)
                return True
        except Exception as e:
            print(f"🔴 Error en escritura: {str(e)}")
            return False
    
    def user_exists(self, username):
        query = f"MATCH (u:User {{username: '{username}'}}) RETURN u"
        result = self._execute_query_with_result(query)
        return bool(result) and len(result) > 0
    
    def register_user(self, username, password):
        if self.user_exists(username):
            return False, "⚠️ El usuario ya existe"
        
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = f"""
        CREATE (u:User {{
            username: '{username}',
            password: '{password}',
            registration_date: '{current_date}'
        }})
        """
        if not self._execute_write_query(query):
            return False, "🔴 Error al registrar usuario"
        
        # --- SELECCIÓN DE ESTILO DURANTE REGISTRO ---
        print("\n" + "="*40)
        print("🎨 ELIGE TU ESTILO PERSONAL")
        print("="*40)
        styles = self.get_all_styles()
        if not styles:
            return True, "✅ Registro completado (sin estilo asignado)"
        
        # Mostrar estilos disponibles
        for i, style in enumerate(styles, 1):
            print(f"\n{i}. {style['nombre'].upper()}")
            print(f"   {style['descripcion']}")
        
        # Selección de estilo
        while True:
            try:
                choice = int(input("\n👉 Selecciona un estilo (número): "))
                if 1 <= choice <= len(styles):
                    selected_style = styles[choice-1]['nombre']
                    if self._save_style_preference(username, selected_style):
                        # --- PREGUNTAR POR RECOMENDACIONES ---
                        print("\n" + "="*40)
                        print(f"🧥 ¿QUIERES RECOMENDACIONES PARA {selected_style.upper()}?")
                        print("="*40)
                        if input("¿Mostrar sugerencias de outfit ahora? (s/n): ").lower() == 's':
                            self._show_style_recommendation(selected_style)
                        return True, f"✅ Registro completado. ¡Bienvenid@ al estilo {selected_style}!"
                    break
                print("🔢 Número fuera de rango")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        return True, "✅ Registro completado"
    
    def _save_style_preference(self, username, style_name):
        # Verificar que existen ambos nodos
        check_query = f"""
        MATCH (u:User {{username: '{username}'}})
        MATCH (s:Estilo {{nombre: '{style_name}'}})
        RETURN COUNT(u) > 0 AND COUNT(s) > 0 AS valid
        """
        if not self._execute_query_with_result(check_query)[0]['valid']:
            print(f"❌ Error: Usuario o estilo '{style_name}' no encontrado")
            return False

        # Eliminar preferencia anterior si existe
        self._execute_write_query(
            f"MATCH (u:User {{username: '{username}'}})-[r:PREFIERE]->() DELETE r"
        )

        # Crear nueva relación
        create_query = f"""
        MATCH (u:User {{username: '{username}'}})
        MATCH (s:Estilo {{nombre: '{style_name}'}})
        MERGE (u)-[:PREFIERE]->(s)
        """
        return self._execute_write_query(create_query)
    
    def _show_style_recommendation(self, style_name):
        recommendations = {
            "Clásico": """
            👔 OUTFIT CLÁSICO:
            • Blazer azul marino
            • Camisa blanca de algodón
            • Pantalones de vestir grises
            • Zapatos Oxford negros
            • Reloj de pulsera elegante""",
            
            "Bohemio": """
            🌸 OUTFIT BOHEMIO:
            • Vestido largo floral
            • Chaleco de crochet
            • Botines de cuero
            • Sombrero de ala ancha
            • Collares étnicos""",
            
            "Deportivo": """
            🏃 OUTFIT DEPORTIVO:
            • Leggings negros
            • Sudadera con capucha
            • Zapatillas deportivas
            • Mochila pequeña
            • Gorra ajustable"""
        }
        
        print("\n" + "="*40)
        print(f"🌟 RECOMENDACIÓN {style_name.upper()}")
        print("="*40)
        print(recommendations.get(style_name, "⚠️ Próximamente más opciones para este estilo"))
        print("\n💡 Consejo: Adapta estas piezas a tu guardarropa personal")
    
    def get_all_styles(self):
        query = "MATCH (s:Estilo) RETURN s.nombre AS nombre, s.descripcion AS descripcion"
        return self._execute_query_with_result(query) or []
    
    def view_user_style(self, username):
        query = f"""
        OPTIONAL MATCH (u:User {{username: '{username}'}})-[:PREFIERE]->(s:Estilo)
        RETURN s.nombre AS nombre, s.descripcion AS descripcion
        """
        result = self._execute_query_with_result(query)
        if result and result[0]['nombre']:
            print(f"\n🎩 TU ESTILO: {result[0]['nombre'].upper()}")
            print(f"📌 {result[0]['descripcion']}")
        else:
            print("\nℹ️ No tienes un estilo asignado")
    
    def change_user_style(self, username):
        print("\n" + "="*40)
        print("🔄 CAMBIAR ESTILO")
        print("="*40)
        styles = self.get_all_styles()
        if not styles:
            print("❌ No hay estilos disponibles")
            return
        
        for i, style in enumerate(styles, 1):
            print(f"{i}. {style['nombre']}")
        
        while True:
            try:
                choice = int(input("\n👉 Nuevo estilo (número): "))
                if 1 <= choice <= len(styles):
                    new_style = styles[choice-1]['nombre']
                    if self._save_style_preference(username, new_style):
                        print(f"\n✨ ¡Estilo cambiado a '{new_style}'!")
                        if input("¿Ver recomendaciones ahora? (s/n): ").lower() == 's':
                            self._show_style_recommendation(new_style)
                    break
                print("🔢 Número fuera de rango")
            except ValueError:
                print("❌ Ingresa un número válido")
    
    def get_user_recommendation(self, username):
        query = f"""
        OPTIONAL MATCH (u:User {{username: '{username}'}})-[:PREFIERE]->(s:Estilo)
        RETURN s.nombre AS style
        """
        result = self._execute_query_with_result(query)
        
        if not result or not result[0]['style']:
            print("\n❌ No tienes un estilo asignado")
            if input("¿Seleccionar uno ahora? (s/n): ").lower() == 's':
                self.change_user_style(username)
            return
        
        self._show_style_recommendation(result[0]['style'])
    
    def login(self, username, password):
        query = f"""
        MATCH (u:User {{username: '{username}', password: '{password}'}})
        RETURN COUNT(u) > 0 AS valid
        """
        result = self._execute_query_with_result(query)
        if result and result[0]['valid']:
            self.current_user = username
            return True
        return False
    
    def close(self):
        self.app.close()