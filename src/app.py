from flask import Flask, request, jsonify, render_template
from models import UserManager
from recommendation_manager import RecommendationManager
from db_connection import Neo4jApp 
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

manager = UserManager()

neo4j = Neo4jApp(
    uri=os.getenv("NEO4J_URI"),
    user=os.getenv("NEO4J_USER"),
    password=os.getenv("NEO4J_PASSWORD")
)
recommender = RecommendationManager(neo4j.driver)

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

@app.route('/estilos')
def estilos():
    return render_template('estilos.html')

@app.teardown_appcontext
def close_neo4j(exception):
    neo4j.close()

@app.route('/api/weather')
def get_weather():
    try:
        res = requests.get("https://wttr.in/?format=%C")
        clima = res.text.strip().lower()

        # Simplificación del clima
        if "sun" in clima:
            clima_label = "soleado"
        elif "rain" in clima:
            clima_label = "lluvioso"
        elif "cloud" in clima:
            clima_label = "nublado"
        else:
            clima_label = "desconocido"

        return jsonify({"clima": clima_label})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    estilo = data.get("estilo")
    clima = data.get("clima")

    if not estilo or not clima:
        return jsonify({"success": False, "message": "Faltan datos"}), 400

    outfits = recommender.get_recommendations(estilo, clima)
    return jsonify({"success": True, "recommendations": outfits})

if __name__ == "__main__":
    app.run(debug=True)
