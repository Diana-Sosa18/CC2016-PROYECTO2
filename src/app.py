from recommendation_manager import RecommendationManager
from db_connection import URI, USER, PASSWORD
from flask import jsonify
from flask import Flask, render_template, request
import requests
import os
import atexit

# Ruta absoluta hacia src/templates
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__)
recommendation_manager = RecommendationManager(URI, USER, PASSWORD)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_weather")
def get_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    # Usamos latitud y longitud para hacer la consulta
    if lat and lon:
        url = f"http://wttr.in/{lat},{lon}?format=%c+%C,+%t,+Precipitación:+%p,+Sensación:+%f"
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Clima desde wttr.in:", response.text)
            return response.text
        else:
            return "❌ No se pudo obtener el clima para las coordenadas brindadas."
    return "⚠️ Coordenadas no recibidas."

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    username = data.get('user')
    estilo = data.get('estilo')
    clima = data.get('clima')
    ocasion = data.get('ocasion')

    # Validar datos mínimos
    if not all([username, estilo, clima, ocasion]):
        return jsonify({"error": "Faltan datos para generar recomendaciones"}), 400

    prendas = recommendation_manager.get_recommendations(username, estilo, clima, ocasion)
    if not prendas:
        return jsonify({"message": "No se encontraron recomendaciones para esos parámetros"}), 404

    return jsonify(prendas)


if __name__ == "__main__":
    app.run(debug=True)

@atexit.register
def shutdown():
    recommendation_manager.close()
