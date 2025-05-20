from flask import Flask, render_template, request
import requests

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
        url = f"http://wttr.in/{lat},{lon}?format=3"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "❌ No se pudo obtener el clima."
    return "⚠️ Coordenadas no recibidas."

if __name__ == "__main__":
    app.run(debug=True)
