import os
import sys
import requests
import PySimpleGUI as sg
from PIL import Image
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from recommendation_manager import RecommendationManager
from db_connection import URI, USER, PASSWORD
from neo4j import GraphDatabase

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

def cargar_imagen(ruta):
    try:
        image = Image.open(ruta)
        image.thumbnail((200, 200))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        return bio.getvalue()
    except Exception as e:
        print(f"Error cargando imagen {ruta}: {e}")
        return None

def mostrar_recomendaciones_gui(recomendaciones):
    image_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))

    layout = []
    for i, outfit in enumerate(recomendaciones, 1):
        image_file = os.path.join(image_folder, outfit["ID_Image"])  # NO agregar ".png"

        if not os.path.exists(image_file):
            print(f"⚠️ Error cargando imagen {image_file}")
            continue

        try:
            image = Image.open(image_file)
            image.thumbnail((200, 200))
            image.save("temp_image.png")
        except Exception as e:
            print(f"⚠️ Error al procesar imagen {image_file}: {e}")
            continue

        layout.append([
            sg.Text(f"Outfit {i}", font=("Helvetica", 14, "bold"))],
        )
        layout.append([
            sg.Image(filename="temp_image.png")
        ])
        layout.append([
            sg.Text(f"Nombre: {outfit['Name']}"),
            sg.Text(f"  Superior: {outfit['Upper']}"),
            sg.Text(f"  Inferior: {outfit['Lower']}"),
            sg.Text(f"  Calzado: {outfit['Footwear']}"),
            sg.Text(f"  Accesorio: {outfit['Accesory']}"),
        ])
        layout.append([
            sg.Button(f"Elegir {i}", key=f"Elegir_{i}")
        ])
        layout.append([sg.HorizontalSeparator()])

    window = sg.Window("Recomendaciones de Outfit", layout, finalize=True)

    outfit_elegido = None
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event and event.startswith("Elegir_"):
            idx = int(event.split("_")[1]) - 1
            outfit_elegido = recomendaciones[idx]
            break

    window.close()
    return outfit_elegido

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

    # Conectar con Neo4j
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    manager = RecommendationManager(driver)

    # Obtener recomendaciones iniciales
    recomendaciones = manager.get_recommendations(estilo_elegido, clima_mapeado)
    if not recomendaciones:
        print("No hay recomendaciones disponibles para estos parámetros.")
        manager.close()
        return

    outfit_elegido = mostrar_recomendaciones_gui(recomendaciones)
    if not outfit_elegido:
        print("No se seleccionó ningún outfit. Saliendo.")
        manager.close()
        return

    historial_nombres = {outfit_elegido["Name"]}

    continuar = True

    while continuar:
        print(f"\n✅ Elegiste el outfit: {outfit_elegido['Name']}")
        nuevos = manager.get_similar_recommendations(outfit_elegido["Name"], estilo_elegido, clima_mapeado, historial_nombres)

        if not nuevos:
            print("❌ No se encontraron más recomendaciones similares.")
            break

        combinados = [outfit_elegido] + nuevos[:2]
        nuevo_elegido = mostrar_recomendaciones_gui(combinados)
        if nuevo_elegido:
            outfit_elegido = nuevo_elegido
            historial_nombres.add(outfit_elegido["Name"])
        else:
            print("👗 ¡Gracias por usar el recomendador de outfits!")
            continuar = False

    manager.close()

if __name__ == "__main__":
    main()
