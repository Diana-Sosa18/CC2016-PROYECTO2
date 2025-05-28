import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from neo4j import GraphDatabase
from recommendation_manager import RecommendationManager
from db_connection import URI, USER, PASSWORD

def obtener_clima_actual():
    try:
        response = requests.get("https://wttr.in/?format=%t+%C")
        if response.status_code == 200:
            datos = response.text.strip()
            temperatura, descripcion = datos.split(" ", 1)
            temperatura = int(temperatura.replace("°C", "").replace("+", ""))
            return temperatura, descripcion
        else:
            print("⚠️ No se pudo obtener el clima actual. Usando clima por defecto.")
            return 20, "Despejado"
    except Exception as e:
        print(f"Error al obtener el clima: {e}")
        return 20, "Despejado"

def mapear_clima(temperatura, descripcion):
    if temperatura >= 25:
        return "Calor Tropical"
    elif temperatura >= 22:
        return "Soleado cálido"
    elif temperatura >= 16:
        return "Templado"
    else:
        return "Frío"

def mostrar_recomendaciones(estilo, clima, manager):
    recomendaciones = manager.get_recommendations(estilo, clima)
    if not recomendaciones:
        print(f"\n❌ No se encontraron recomendaciones para el estilo '{estilo}' y clima '{clima}'.")
        return
    print(f"\n👕 Recomendaciones para estilo *{estilo}* y clima *{clima}*:\n")
    for i, outfit in enumerate(recomendaciones[:3], 1):
        print(f"🔹 Outfit {i}:")
        print(f"   - Superior: {outfit['Upper']}")
        print(f"   - Inferior: {outfit['Lower']}")
        print(f"   - Calzado: {outfit['Footwear']}")
        print(f"   - Accesorio: {outfit['Accesory']}")
        print(f"   - Imagen ID: {outfit['ID_Image']}\n")

def main():
    estilos_disponibles = ["Hipster", "Elegante", "Vintage"]
    print("🎨 ¿Qué estilo prefieres hoy?")
    for idx, estilo in enumerate(estilos_disponibles, 1):
        print(f"{idx}. {estilo}")
    
    while True:
        opcion = input("Selecciona una opción (1-3): ")
        if opcion in ["1", "2", "3"]:
            estilo_elegido = estilos_disponibles[int(opcion) - 1]
            break
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

    temperatura, descripcion = obtener_clima_actual()
    clima_mapeado = mapear_clima(temperatura, descripcion)

    print(f"\n☀️ Clima detectado: {temperatura}°C - {descripcion}")
    print(f"🗺️  Clima mapeado en base de datos: {clima_mapeado}")

    # Crear conexión y manager
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    manager = RecommendationManager(driver)

    # Mostrar recomendaciones
    mostrar_recomendaciones(estilo_elegido, clima_mapeado, manager)

    # Cerrar conexión
    manager.close()

if __name__ == "__main__":
    main()
