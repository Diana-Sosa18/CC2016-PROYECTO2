#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
✨ RECOMENDADOR DE OUTFITS PARA GUATEMALA ✨
Sistema inteligente que recomienda outfits basado en:
- Estilo personal preferido
- Ocasión especial
- Clima actual 
"""

import sys
import os
import requests
from colorama import init, Fore, Back, Style
init(autoreset=True)  # Initialize colorama

# Configure path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from neo4j import GraphDatabase
from recommendation_manager import RecommendationManager
from db_connection import URI, USER, PASSWORD
from models import UserManager

# 🌤️ WEATHER FUNCTIONS 🌤️
def obtener_clima_actual():
    """Obtiene la temperatura actual"""
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
        
        print(Fore.YELLOW + "⚠️  No se pudo obtener el clima. Usando temperatura por defecto (22°C).")
        return 22
    
    except Exception as e:
        print(Fore.RED + f"⚠️  Error al obtener el clima: {e}")
        return 22

def mapear_clima(temperatura):
    """Mapea la temperatura a categorías de clima"""
    if temperatura >= 28:
        return "Calor Tropical"
    elif temperatura >= 23:
        return "Soleado cálido"
    elif temperatura >= 16:
        return "Templado"
    else:
        return "Frío"

# 👗 RECOMMENDATION FUNCTIONS 👗
def mostrar_recomendaciones_y_seleccionar(manager, estilo, ocasion, clima):
    """Muestra recomendaciones y maneja la selección del usuario"""
    historial_outfits = set()
    
    while True:
        # Get new recommendations (excluding already shown)
        nuevos_outfits = [
            o for o in manager.get_recommendations(estilo, clima, ocasion)
            if o['Name'] not in historial_outfits
        ][:3]
        
        if not nuevos_outfits:
            print(Fore.RED + "\n❌ No hay más outfits disponibles con estos filtros.")
            return None

        # Display recommendations
        print(Fore.CYAN + Style.BRIGHT + f"\n👕 Outfits recomendados para:")
        print(Fore.MAGENTA + f"   Estilo: {estilo}")
        print(Fore.GREEN + f"   Ocasión: {ocasion}")
        print(Fore.BLUE + f"   Clima: {clima}\n")
        
        for i, o in enumerate(nuevos_outfits, 1):
            print(Fore.YELLOW + Style.BRIGHT + f"🌟 {i}. {o['Name']}")
            print(Fore.WHITE + f"   - 👕 Superior: {o['Upper']}")
            print(Fore.WHITE + f"   - 👖 Inferior: {o['Lower']}")
            print(Fore.WHITE + f"   - 👟 Calzado: {o['Footwear']}")
            historial_outfits.add(o['Name'])

        # User selection
        while True:
            seleccion = input(Fore.MAGENTA + "\n👉 Elige un outfit (1-3), 'm' para más opciones o 's' para salir: ").strip().lower()
            
            if seleccion == 's':
                return None
            elif seleccion == 'm':
                break
            elif seleccion in {'1', '2', '3'}:
                return nuevos_outfits[int(seleccion)-1]
            else:
                print(Fore.RED + "❌ Opción no válida. Intenta nuevamente.")

# 🎯 MAIN FUNCTION 🎯
def main():
    # Welcome message
    print(Fore.CYAN + Style.BRIGHT + "="*50)
    print(Fore.YELLOW + "✨  PÓNTELO!  👗")
    print(Fore.CYAN + "="*50)
    print(Fore.WHITE + "👋 ¡Bienvenid@!\n")
    
    # Setup services
    user_manager = UserManager()
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    manager = RecommendationManager(driver)

    try:
        # --- AUTHENTICATION ---
        while True:
            print(Fore.GREEN + Style.BRIGHT + "\n🔐 MENÚ DE AUTENTICACIÓN")
            print(Fore.CYAN + "1. 🔑 Iniciar sesión")
            print(Fore.CYAN + "2. 📝 Registrarse")
            print(Fore.CYAN + "3. 🚪 Salir")
            
            opcion = input(Fore.MAGENTA + "\n👉 Selecciona una opción (1-3): ").strip()

            if opcion == "1":
                username = input(Fore.BLUE + "Nombre de usuario: ").strip()
                password = input(Fore.BLUE + "Contraseña: ").strip()
                if user_manager.login(username, password):
                    print(Fore.GREEN + f"\n✅ ¡Bienvenido de nuevo, {username}!")
                    break
                print(Fore.RED + "\n❌ Credenciales incorrectas.")
            elif opcion == "2":
                username = input(Fore.BLUE + "Elige un nombre de usuario: ").strip()
                password = input(Fore.BLUE + "Crea una contraseña: ").strip()
                success, msg = user_manager.register_user(username, password)
                print(Fore.GREEN + "\n✅ " + msg if success else Fore.RED + "❌ " + msg)
                if success: break
            elif opcion == "3":
                print(Fore.YELLOW + "\n👋 ¡Hasta pronto!")
                return
            else:
                print(Fore.RED + "\n❌ Opción no válida.")

        # --- MAIN LOOP ---
        while True:
            # --- STYLE SELECTION ---
            print(Fore.CYAN + Style.BRIGHT + "\n🎨 ¿Qué estilo de outfit prefieres?")
            estilos = ["🎨 Hipster", "👔 Elegante", "🕰️ Vintage"]
            for i, estilo in enumerate(estilos, 1):
                print(Fore.BLUE + f"{i}. {estilo}")
            
            while True:
                opcion = input(Fore.MAGENTA + "\n👉 Elige un estilo (1-3): ").strip()
                if opcion in {"1", "2", "3"}:
                    estilo = estilos[int(opcion)-1].split()[1]  # Remove emoji
                    break
                print(Fore.RED + "❌ Opción no válida.")

            # --- OCCASION SELECTION --- 
            print(Fore.CYAN + Style.BRIGHT + "\n🎉 ¿Para qué ocasión es el outfit?")
            ocasiones = ["💼 Trabajo", "🎓 Universidad", "🎉 Fiesta"]
            for i, ocasion in enumerate(ocasiones, 1):
                print(Fore.BLUE + f"{i}. {ocasion}")
            
            while True:
                opcion = input(Fore.MAGENTA + "\n👉 Elige una ocasión (1-3): ").strip()
                if opcion in {"1", "2", "3"}:
                    ocasion = ocasiones[int(opcion)-1].split()[1]  # Remove emoji
                    break
                print(Fore.RED + "❌ Opción no válida.")

            # --- GET WEATHER ---
            temperatura = obtener_clima_actual()
            clima = mapear_clima(temperatura)
            print(Fore.CYAN + "\n📍 Ubicación: Ciudad de Guatemala")
            print(Fore.CYAN + f"🌡️  Temperatura actual: {Fore.YELLOW}{temperatura}°C")
            print(Fore.CYAN + f"☀️  Clima categorizado: {Fore.GREEN}{clima}")

            # --- GENERATE RECOMMENDATIONS ---
            outfit_elegido = mostrar_recomendaciones_y_seleccionar(manager, estilo, ocasion, clima.split()[-1])
            
            if outfit_elegido:
                print(Fore.GREEN + Style.BRIGHT + "\n🎉 ¡Felicidades por tu elección!")
                print(Fore.YELLOW + f"\n✨ Outfit seleccionado: {outfit_elegido['Name']}")
                print(Fore.WHITE + f"👕 Superior: {outfit_elegido['Upper']}")
                print(Fore.WHITE + f"👖 Inferior: {outfit_elegido['Lower']}")
                print(Fore.WHITE + f"👟 Calzado: {outfit_elegido['Footwear']}")
            else:
                print(Fore.CYAN + "\nVolviendo al menú principal...")

    finally:
        manager.close()
        user_manager.close()

if __name__ == "__main__":
    main()