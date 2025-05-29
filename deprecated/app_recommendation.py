#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌈 RECOMENDADOR INTELIGENTE DE OUTFITS 🌈
Sistema que recomienda combinaciones de ropa según:
- Estilo personal (Hipster, Elegante, Vintage)
- Clima actual (obtenido de API meteorológica)
- Base de datos Neo4j con relaciones entre prendas
"""

import sys
import os
import requests
from colorama import init, Fore, Back, Style
from flask import Flask, render_template
from neo4j import GraphDatabase
from recommendation_manager import RecommendationManager
from db_connection import URI, USER, PASSWORD

# Inicialización de colorama para colores en terminal
init(autoreset=True)

# 🌤️ FUNCIÓN PARA OBTENER CLIMA ACTUAL 🌤️
def obtener_clima_actual():
    """
    Obtiene el clima actual desde wttr.in
    Returns:
        tuple: (temperatura, descripción)
    """
    try:
        response = requests.get("https://wttr.in/?format=%t+%C")
        if response.status_code == 200:
            datos = response.text.strip()
            temperatura, descripcion = datos.split(" ", 1)
            temperatura = int(temperatura.replace("°C", "").replace("+", ""))
            return temperatura, descripcion
        else:
            print(Fore.YELLOW + "⚠️  No se pudo obtener el clima actual. Usando clima por defecto.")
            return 20, "Despejado"
    except Exception as e:
        print(Fore.RED + f"❌ Error al obtener el clima: {e}")
        return 20, "Despejado"

# 🌡️ FUNCIÓN PARA MAPEAR CLIMA A CATEGORÍAS 🌡️
def mapear_clima(temperatura, descripcion):
    """
    Clasifica el clima en categorías para recomendaciones
    Args:
        temperatura (int): Temperatura en °C
        descripcion (str): Descripción del clima
    Returns:
        str: Categoría de clima
    """
    if temperatura >= 25:
        return "🔥 Calor Tropical"
    elif temperatura >= 22:
        return "☀️ Soleado cálido"
    elif temperatura >= 16:
        return "🌤️ Templado"
    else:
        return "❄️ Frío"

# 👗 FUNCIÓN PARA MOSTRAR RECOMENDACIONES 👗
def mostrar_recomendaciones(estilo, clima, manager):
    """
    Muestra outfits recomendados con formato bonito
    Args:
        estilo (str): Estilo de ropa
        clima (str): Categoría de clima
        manager (RecommendationManager): Gestor de recomendaciones
    Returns:
        list: Lista de recomendaciones
    """
    recomendaciones = manager.get_recommendations(estilo, clima)
    if not recomendaciones:
        print(Fore.RED + f"\n❌ No se encontraron recomendaciones para {Fore.MAGENTA}{estilo}{Fore.RED} y clima {Fore.CYAN}{clima}")
        return []
    
    print(Fore.GREEN + Style.BRIGHT + f"\n✨ 👗 RECOMENDACIONES PARA:")
    print(Fore.MAGENTA + f"   Estilo: {estilo}")
    print(Fore.CYAN + f"   Clima: {clima}\n")
    
    for i, outfit in enumerate(recomendaciones[:3], 1):
        print(Fore.BLUE + Style.BRIGHT + f"🌟 OUTFIT {i}:")
        print(Fore.WHITE + f"   - 📛 {Fore.YELLOW}Nombre: {outfit['Name']}")
        print(Fore.WHITE + f"   - 👚 {Fore.YELLOW}Superior: {outfit['Upper']}")
        print(Fore.WHITE + f"   - 👖 {Fore.YELLOW}Inferior: {outfit['Lower']}")
        print(Fore.WHITE + f"   - 👟 {Fore.YELLOW}Calzado: {outfit['Footwear']}")
        print(Fore.WHITE + f"   - 🕶️  {Fore.YELLOW}Accesorio: {outfit['Accesory']}")
        print(Fore.WHITE + f"   - 🖼️  {Fore.YELLOW}Imagen ID: {outfit['ID_Image']}\n")
    return recomendaciones[:3]

# 🔘 FUNCIÓN PARA ELEGIR OUTFIT 🔘
def elegir_outfit(recomendaciones):
    """
    Permite al usuario seleccionar un outfit
    Args:
        recomendaciones (list): Lista de outfits
    Returns:
        dict: Outfit seleccionado
    """
    while True:
        seleccion = input(Fore.MAGENTA + "👉 Ingresa el número del outfit que más te gusta (1-3): ")
        if seleccion in ["1", "2", "3"]:
            return recomendaciones[int(seleccion) - 1]
        print(Fore.RED + "❌ Selección inválida. Intenta de nuevo.")

# 🎯 FUNCIÓN PRINCIPAL 🎯
def main():
    """Función principal que orquesta el flujo del programa"""
    
    # Configuración inicial
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
    
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*50)
    print(Fore.YELLOW + "🌈  RECOMENDADOR INTELIGENTE DE OUTFITS  👗")
    print(Fore.CYAN + "="*50)
    
    # Selección de estilo
    estilos_disponibles = ["🎨 Hipster", "👔 Elegante", "🕰️ Vintage"]
    print(Fore.GREEN + "\n🎨 ¿Qué estilo prefieres hoy?")
    for idx, estilo in enumerate(estilos_disponibles, 1):
        print(Fore.BLUE + f"{idx}. {estilo}")
    
    while True:
        opcion = input(Fore.MAGENTA + "\n👉 Selecciona una opción (1-3): ")
        if opcion in ["1", "2", "3"]:
            estilo_elegido = estilos_disponibles[int(opcion) - 1].split()[1]
            break
        else:
            print(Fore.RED + "❌ Opción no válida. Intenta de nuevo.")

    # Obtención de clima
    temperatura, descripcion = obtener_clima_actual()
    clima_mapeado = mapear_clima(temperatura, descripcion)

    print(Fore.CYAN + f"\n🌤️  Clima detectado: {Fore.YELLOW}{temperatura}°C - {descripcion}")
    print(Fore.CYAN + f"🗺️  Clima mapeado: {Fore.GREEN}{clima_mapeado}")

    # Conexión a Neo4j
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    manager = RecommendationManager(driver)

    # Primera ronda de recomendaciones
    recomendaciones = mostrar_recomendaciones(estilo_elegido, clima_mapeado.split()[-1], manager)
    if not recomendaciones:
        manager.close()
        return

    outfit_elegido = elegir_outfit(recomendaciones)
    historial_nombres = {outfit_elegido["Name"]}

    # Bucle de recomendaciones adicionales
    continuar = True
    while continuar:
        print(Fore.GREEN + f"\n🎉 ¡Elegiste el outfit: {Fore.YELLOW}{outfit_elegido['Name']}")
        nuevos = manager.get_similar_recommendations(
            outfit_elegido["Name"], 
            estilo_elegido, 
            clima_mapeado.split()[-1], 
            historial_nombres
        )

        if not nuevos:
            print(Fore.RED + "❌ No se encontraron más recomendaciones similares.")
            break

        # Mostrar nuevas opciones
        combinados = [outfit_elegido] + nuevos[:2]
        for i, outfit in enumerate(combinados, 1):
            print(Fore.BLUE + Style.BRIGHT + f"\n🌟 OUTFIT {i}:")
            print(Fore.WHITE + f"   - 📛 {Fore.YELLOW}Nombre: {outfit['Name']}")
            print(Fore.WHITE + f"   - 👚 {Fore.YELLOW}Superior: {outfit['Upper']}")
            print(Fore.WHITE + f"   - 👖 {Fore.YELLOW}Inferior: {outfit['Lower']}")
            print(Fore.WHITE + f"   - 👟 {Fore.YELLOW}Calzado: {outfit['Footwear']}")
            print(Fore.WHITE + f"   - 🕶️  {Fore.YELLOW}Accesorio: {outfit['Accesory']}")
            print(Fore.WHITE + f"   - 🖼️  {Fore.YELLOW}Imagen ID: {outfit['ID_Image']}")

        seleccion = input(Fore.MAGENTA + "\n👉 ¿Deseas ver más recomendaciones similares? (s/n): ").strip().lower()
        if seleccion == "s":
            outfit_elegido = elegir_outfit(combinados)
            historial_nombres.add(outfit_elegido["Name"])
        else:
            print(Fore.CYAN + Style.BRIGHT + "\n👗 ¡Gracias por usar el recomendador de outfits! 💖")
            continuar = False

    manager.close()

# 🖥️ CONFIGURACIÓN FLASK 🖥️
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    """Ruta principal de la aplicación web"""
    return render_template('index.html')

if __name__ == "__main__":
    # Ejecutar tanto la interfaz CLI como la web
    main()
    app.run(debug=True)