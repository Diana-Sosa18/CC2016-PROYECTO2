from flask import Flask, render_template, requests, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_weather")
def get_weather():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")

    # Usamos latitud y longitud para hacer la consulta
    if latitude and longitude:
        url = f"http://wttr.in/{latitude},{longitude}?format=3"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "❌ No se pudo obtener el clima para las coordenadas brindadas."
    return "⚠️ Coordenadas no recibidas."

if __name__ == "__main__":
    app.run(debug=True)
