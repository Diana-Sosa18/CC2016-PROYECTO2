from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import UserManager
from neo4j import GraphDatabase, basic_auth
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

# Inicializar UserManager
manager = UserManager()

# Conexión a Neo4j con variables de entorno
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

try:
    driver = GraphDatabase.driver(uri, auth=basic_auth(username, password))
    with driver.session() as session:
        session.run("RETURN 1")
    print("✅ Conexión exitosa con la base de datos Neo4j.")
except Exception as e:
    print("❌ Error al conectar con la base de datos Neo4j:", e)
    driver = None

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"success": False, "message": "Faltan datos"}), 400

    success, message = manager.register_user(username, password)
    return jsonify({"success": success, "message": message})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not manager.login(username, password):
        return jsonify({"success": False, "message": "Usuario o contraseña incorrectos"}), 401
    return jsonify({"success": True, "message": "Inicio de sesión exitoso"}), 200


@app.route('/')
def home():
    return render_template('index.html')

# Puedes definir tu ruta estilos aquí si aún no la has hecho
@app.route('/estilos')
def estilos():
    return render_template('estilos.html')

if __name__ == "__main__":
    app.run(debug=True)
