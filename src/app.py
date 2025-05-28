from flask import Flask, render_template, request
import requests
import os

# Ruta absoluta hacia src/templates
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
