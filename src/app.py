import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from neo4j import GraphDatabase
from recommendation_manager import RecommendationManager
from db_connection import URI, USER, PASSWORD
from models import UserManager

def obtener_clima_actual():
    try:
        # Usamos un User-Agent para evitar bloqueos y parámetros más robustos
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get("https://wttr.in/?format=%t+%C", headers=headers, timeout=10)
        
        if response.status_code == 200:
            datos = response.text.strip()
            # Manejo más robusto de la respuesta
            if " " in datos:
                temperatura, descripcion = datos.split(" ", 1)
                # Limpieza de la temperatura
                temperatura = temperatura.replace("°C", "").replace("+", "").strip()
                try:
                    temperatura = int(temperatura)
                    return temperatura, descripcion
                except ValueError:
                    print("⚠️ Formato de temperatura inválido. Usando clima por defecto.")
            else:
                print("⚠️ Respuesta de la API inesperada. Usando clima por defecto.")
        else:
            print(f"⚠️ Error en la API del clima (código {response.status_code}). Usando clima por defecto.")
            
        return 20, "Despejado"
    
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error de conexión al obtener el clima: {e}. Usando clima por defecto.")
        return 20, "Despejado"
    except Exception as e:
        print(f"⚠️ Error inesperado al obtener el clima: {e}. Usando clima por defecto.")
        return 20, "Despejado"

def mapear_clima(temperatura, descripcion):
    descripcion = descripcion.lower()
    
    # Primero verificamos condiciones específicas en la descripción
    if "lluvia" in descripcion or "rain" in descripcion:
        return "Lluvioso"
    elif "nieve" in descripcion or "snow" in descripcion:
        return "Nevado"
    
    # Luego verificamos por temperatura
    if temperatura >= 28:
        return "Calor Tropical"
    elif temperatura >= 23:
        return "Soleado cálido"
    elif temperatura >= 18:
        return "Templado"
    elif temperatura >= 10:
        return "Frío"
    else:
        return "Muy frío"

def mostrar_recomendaciones(estilo, clima, manager):
    recomendaciones = manager.get_recommendations(estilo, clima)
    if not recomendaciones:
        print(f"\n❌ No se encontraron recomendaciones para el estilo '{estilo}' y clima '{clima}'.")
        return []
    
    print(f"\n👕 Recomendaciones para estilo *{estilo}* y clima *{clima}*:\n")
    for i, outfit in enumerate(recomendaciones[:3], 1):
        print(f"🔹 Outfit {i}:")
        print(f"   - Nombre: {outfit['Name']}")
        print(f"   - Superior: {outfit['Upper']}")
        print(f"   - Inferior: {outfit['Lower']}")
        print(f"   - Calzado: {outfit['Footwear']}")
        print(f"   - Accesorio: {outfit['Accesory']}")
        print(f"   - Imagen ID: {outfit['ID_Image']}\n")
    return recomendaciones[:3]

def elegir_outfit(recomendaciones):
    while True:
        seleccion = input("👉 Ingresa el número del outfit que más te gusta (1-3): ").strip()
        if seleccion in {"1", "2", "3"}:
            return recomendaciones[int(seleccion) - 1]
        print("❌ Selección inválida. Intenta de nuevo.")

def main():
    
    print("👋 ¡Bienvenido al recomendador de outfits!\n")
    user_manager = UserManager()

    while True:
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Selecciona una opción (1, 2 o 3): ").strip()

        if opcion == "1":
            username = input("Nombre de usuario: ").strip()
            password = input("Contraseña: ").strip()
            if user_manager.login(username, password):
                print(f"✅ ¡Bienvenido de nuevo, {username}!")
                break
            else:
                print("❌ Nombre de usuario o contraseña incorrectos.")
        elif opcion == "2":
            username = input("Elige un nombre de usuario: ").strip()
            password = input("Crea una contraseña: ").strip()
            success, mensaje = user_manager.register_user(username, password)
            print("✅ " + mensaje if success else "❌ " + mensaje)
            if success:
                break
        elif opcion == "3":
            print("👋 ¡Hasta pronto!")
            user_manager.close()
            return
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

    # Conectar con Neo4j
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    manager = RecommendationManager(driver)

    try:
        while True:
            estilos_disponibles = ["Hipster", "Elegante", "Vintage"]
            print("\n🎨 ¿Qué estilo prefieres hoy?")
            for idx, estilo in enumerate(estilos_disponibles, 1):
                print(f"{idx}. {estilo}")
            
            while True:
                opcion = input("Selecciona una opción (1-3): ").strip()
                if opcion in {"1", "2", "3"}:
                    estilo_elegido = estilos_disponibles[int(opcion) - 1]
                    break
                print("❌ Opción no válida. Intenta de nuevo.")

            temperatura, descripcion = obtener_clima_actual()
            clima_mapeado = mapear_clima(temperatura, descripcion)

            print(f"\n🌡️  Temperatura actual: {temperatura}°C")
            print(f"☁️  Condiciones: {descripcion}")
            print(f"🗺️  Clima mapeado: {clima_mapeado}")

            recomendaciones = mostrar_recomendaciones(estilo_elegido, clima_mapeado, manager)
            if not recomendaciones:
                continue

            outfit_elegido = elegir_outfit(recomendaciones)
            historial_nombres = {outfit_elegido["Name"]}

            while True:
                print(f"\n✅ Elegiste el outfit: {outfit_elegido['Name']}")
                seleccion = input("\n👉 ¿Deseas ver más recomendaciones similares? (s/n): ").strip().lower()
                
                if seleccion != "s":
                    print("\n🎉 ¡Felicidades! Tu outfit ideal es:")
                    print(f"   - Nombre: {outfit_elegido['Name']}")
                    print(f"   - Superior: {outfit_elegido['Upper']}")
                    print(f"   - Inferior: {outfit_elegido['Lower']}")
                    print(f"   - Calzado: {outfit_elegido['Footwear']}")
                    print(f"   - Accesorio: {outfit_elegido['Accesory']}")
                    print(f"   - Imagen ID: {outfit_elegido['ID_Image']}")
                    break

                nuevos = manager.get_similar_recommendations(
                    outfit_elegido["Name"], estilo_elegido, clima_mapeado, historial_nombres)

                if not nuevos:
                    print("❌ No se encontraron más recomendaciones similares.")
                    break

                combinados = [outfit_elegido] + nuevos[:2]
                for i, outfit in enumerate(combinados, 1):
                    print(f"\n🔹 Outfit {i}:")
                    print(f"   - Nombre: {outfit['Name']}")
                    print(f"   - Imagen ID: {outfit['ID_Image']}")

                outfit_elegido = elegir_outfit(combinados)
                historial_nombres.add(outfit_elegido["Name"])
    finally:
        manager.close()
        user_manager.close()
    
if __name__ == "__main__":
    main()