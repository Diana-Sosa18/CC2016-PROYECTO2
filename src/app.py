import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from neo4j import GraphDatabase
from recommendation_manager import RecommendationManager
from db_connection import URI, USER, PASSWORD
from models import UserManager

def obtener_clima_actual():
    """Obtiene el clima actual para Ciudad de Guatemala"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = "https://wttr.in/Ciudad+de+Guatemala?format=%t"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            temperatura = response.text.strip()
            temperatura = temperatura.replace("°C", "").replace("+", "").strip()
            try:
                return int(temperatura)
            except ValueError:
                pass
        
        print("⚠️ No se pudo obtener el clima. Usando temperatura por defecto (22°C).")
        return 22
    
    except Exception as e:
        print(f"⚠️ Error al obtener el clima: {e}")
        return 22

def mapear_clima(temperatura):
    """Mapea la temperatura a las 4 categorías soportadas"""
    if temperatura >= 28:
        return "Calor Tropical"
    elif temperatura >= 23:
        return "Soleado cálido"
    elif temperatura >= 16:
        return "Templado"
    else:
        return "Frío"

def mostrar_recomendaciones_y_seleccionar(manager, estilo, ocasion, clima):
    """Muestra recomendaciones y maneja la selección del usuario"""
    historial_outfits = set()
    
    while True:
        # Obtener nuevas recomendaciones (excluyendo las ya mostradas)
        nuevos_outfits = [
            o for o in manager.get_recommendations(estilo, clima, ocasion)
            if o['Name'] not in historial_outfits
        ][:3]
        
        if not nuevos_outfits:
            print("\n❌ No hay más outfits disponibles con estos filtros.")
            return None

        # Mostrar recomendaciones
        print(f"\n👕 Outfits recomendados para {estilo} ({ocasion}, {clima}):")
        for i, o in enumerate(nuevos_outfits, 1):
            print(f"\n🔹 {i}. {o['Name']}")
            print(f"   - Superior: {o['Upper']}")
            print(f"   - Inferior: {o['Lower']}")
            print(f"   - Calzado: {o['Footwear']}")
            historial_outfits.add(o['Name'])

        # Selección del usuario
        while True:
            seleccion = input("\n👉 Elige un outfit (1-3), 'm' para más opciones o 's' para salir: ").strip().lower()
            
            if seleccion == 's':
                return None
            elif seleccion == 'm':
                break  # Salir del bucle interno para mostrar más opciones
            elif seleccion in {'1', '2', '3'}:
                return nuevos_outfits[int(seleccion)-1]
            else:
                print("❌ Opción no válida. Intenta nuevamente.")

def main():
    print("👋 ¡Bienvenido al recomendador de outfits para Guatemala!\n")
    
    # Configurar servicios
    user_manager = UserManager()
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    manager = RecommendationManager(driver)

    try:
        # --- AUTENTICACIÓN ---
        while True:
            print("1. Iniciar sesión\n2. Registrarse\n3. Salir")
            opcion = input("Selecciona una opción (1-3): ").strip()

            if opcion == "1":
                username = input("Nombre de usuario: ").strip()
                password = input("Contraseña: ").strip()
                if user_manager.login(username, password):
                    print(f"\n✅ ¡Bienvenido de nuevo, {username}!")
                    break
                print("\n❌ Credenciales incorrectas.")
            elif opcion == "2":
                username = input("Elige un nombre de usuario: ").strip()
                password = input("Crea una contraseña: ").strip()
                success, msg = user_manager.register_user(username, password)
                print("\n✅ " + msg if success else "❌ " + msg)
                if success: break
            elif opcion == "3":
                print("\n👋 ¡Hasta pronto!")
                return
            else:
                print("\n❌ Opción no válida.")

        # --- BUCLE PRINCIPAL ---
        while True:
            # --- SELECCIÓN DE ESTILO ---
            print("\n🎨 ¿Qué estilo de outfit prefieres?")
            estilos = ["Hipster", "Elegante", "Vintage"]
            for i, estilo in enumerate(estilos, 1):
                print(f"{i}. {estilo}")
            
            while True:
                opcion = input("\nElige un estilo (1-3): ").strip()
                if opcion in {"1", "2", "3"}:
                    estilo = estilos[int(opcion)-1]
                    break
                print("❌ Opción no válida.")

            # --- SELECCIÓN DE OCASIÓN --- 
            print("\n🎉 ¿Para qué ocasión es el outfit?")
            ocasiones = ["Trabajo", "Universidad", "Fiesta"]  # Solo estas 3 opciones
            for i, ocasion in enumerate(ocasiones, 1):
                print(f"{i}. {ocasion}")
            
            while True:
                opcion = input("\nElige una ocasión (1-3): ").strip()
                if opcion in {"1", "2", "3"}:
                    ocasion = ocasiones[int(opcion)-1]
                    break
                print("❌ Opción no válida.")

            # --- OBTENER CLIMA ---
            temperatura = obtener_clima_actual()
            clima = mapear_clima(temperatura)
            print(f"\n📍 Ubicación: Ciudad de Guatemala")
            print(f"🌡️  Temperatura actual: {temperatura}°C")
            print(f"☀️  Clima categorizado: {clima}")

            # --- GENERAR RECOMENDACIONES ---
            outfit_elegido = mostrar_recomendaciones_y_seleccionar(manager, estilo, ocasion, clima)
            
            if outfit_elegido:
                print("\n🎉 ¡Felicidades por tu elección!")
                print(f"\n✨ Outfit seleccionado: {outfit_elegido['Name']}")
                print(f"👕 Superior: {outfit_elegido['Upper']}")
                print(f"👖 Inferior: {outfit_elegido['Lower']}")
                print(f"👟 Calzado: {outfit_elegido['Footwear']}")
            else:
                print("\nVolviendo al menú principal...")

    finally:
        manager.close()
        user_manager.close()

if __name__ == "__main__":
    main()