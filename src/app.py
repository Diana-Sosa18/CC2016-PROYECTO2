import sys
import os
import requests
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import tempfile
from colorama import Fore, Style, init
init(autoreset=True)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from neo4j import GraphDatabase
from recommendation_manager import RecommendationManager
from db_connection import URI, USER, PASSWORD
from models import UserManager

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

def mostrar_imagenes_outfits(outfits, images_folder='images'):
    """Muestra los outfits reales desde la carpeta de imágenes con mejor formato visual"""
    num_outfits = min(3, len(outfits))
    if num_outfits == 0:
        return
    
    fig, axs = plt.subplots(1, num_outfits, figsize=(18, 6))
    

    if num_outfits == 1:
        axs = [axs]
    

    try:
        font_title = ImageFont.truetype("arial.ttf", 22)
        font_text = ImageFont.truetype("arial.ttf", 18)
    except IOError:
        font_title = None
        font_text = None
    
    for i, outfit in enumerate(outfits[:3]):
        try:
            image_path = os.path.join(images_folder, f"{outfit['ID_Image']}")
            img = Image.open(image_path)
            axs[i].imshow(img)
            axs[i].axis('off')
            axs[i].set_title(f"OPCIÓN {i+1}", fontsize=16, fontweight='bold', color="#221E1E")
        except Exception as e:
            print(f"⚠️ No se pudo cargar la imagen para {outfit['Name']}: {e}")
            img = Image.new('RGB', (350, 450), color=(73, 109, 137))
            d = ImageDraw.Draw(img)

            y_text = 15
            spacing = 35
            if font_title:
                d.text((10, y_text), f"Outfit: {outfit['Name']}", font=font_title, fill=(255, 255, 0))
                y_text += spacing
                d.text((10, y_text), f"Superior: {outfit['Upper']}", font=font_text, fill=(255, 255, 255))
                y_text += spacing
                d.text((10, y_text), f"Inferior: {outfit['Lower']}", font=font_text, fill=(255, 255, 255))
                y_text += spacing
                d.text((10, y_text), f"Calzado: {outfit['Footwear']}", font=font_text, fill=(255, 255, 255))
            else:
                d.text((10, y_text), f"Outfit: {outfit['Name']}", fill=(255, 255, 0))
                y_text += spacing
                d.text((10, y_text), f"Superior: {outfit['Upper']}", fill=(255, 255, 255))
                y_text += spacing
                d.text((10, y_text), f"Inferior: {outfit['Lower']}", fill=(255, 255, 255))
                y_text += spacing
                d.text((10, y_text), f"Calzado: {outfit['Footwear']}", fill=(255, 255, 255))
            
            axs[i].imshow(img)
            axs[i].axis('off')
    
    plt.tight_layout(rect=[0, 0, 1, 0.92])  
    plt.show(block=False)
    plt.pause(0.1)


def obtener_clima_actual():
    """Obtiene el clima actual para Ciudad de Guatemala"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = "https://wttr.in/Ciudad+de+Guatemala?format=%t"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            temperatura = response.text.strip().replace("°C", "").replace("+", "").strip()
            return int(temperatura)
        print("⚠️ No se pudo obtener el clima. Usando temperatura por defecto (22°C).")
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

# 👗 RECOMMENDATION FUNCTIONS 👗
def mostrar_recomendaciones_y_seleccionar(manager, estilo, ocasion, clima):
    """Muestra recomendaciones y maneja la selección del usuario"""
    historial_outfits = set()
    
    while True:
        nuevos_outfits = [
            o for o in manager.get_recommendations(estilo, clima, ocasion)
            if o['Name'] not in historial_outfits
        ][:3]
        
        if not nuevos_outfits:
            print(Fore.RED + "\n❌ No hay más outfits disponibles con estos filtros.")
            return None

        mostrar_imagenes_outfits(nuevos_outfits)

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
    print(Fore.CYAN + Style.BRIGHT + "="*50)
    print(Fore.YELLOW + "✨  PÓNTELO!  👗")
    print(Fore.CYAN + "="*50)
    print(Fore.WHITE + "👋 ¡Bienvenid@!\n")
    
    user_manager = UserManager()
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    manager = RecommendationManager(driver)

    try:
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

        while True:
            print(Fore.CYAN + Style.BRIGHT + "\n🎨 ¿Qué estilo de outfit prefieres?")
            estilos = ["🎨 Hipster", "👔 Elegante", "🕰️ Vintage"]
            for i, estilo in enumerate(estilos, 1):
                print(Fore.BLUE + f"{i}. {estilo}")
            
            while True:
                opcion = input(Fore.MAGENTA + "\n👉 Elige un estilo (1-3): ").strip()
                if opcion in {"1", "2", "3"}:
                    estilo = estilos[int(opcion)-1].split()[1]  
                    break
                print(Fore.RED + "❌ Opción no válida.")

            print(Fore.CYAN + Style.BRIGHT + "\n🎉 ¿Para qué ocasión es el outfit?")
            ocasiones = ["💼 Trabajo", "🎓 Universidad", "🎉 Fiesta"]
            for i, ocasion in enumerate(ocasiones, 1):
                print(Fore.BLUE + f"{i}. {ocasion}")
            
            while True:
                opcion = input(Fore.MAGENTA + "\n👉 Elige una ocasión (1-3): ").strip()
                if opcion in {"1", "2", "3"}:
                    ocasion = ocasiones[int(opcion)-1].split()[1]
                    break
                print(Fore.RED + "❌ Opción no válida.")

            temperatura = obtener_clima_actual()
            clima = mapear_clima(temperatura)
            print(Fore.CYAN + "\n📍 Ubicación: Ciudad de Guatemala")
            print(Fore.CYAN + f"🌡️  Temperatura actual: {Fore.YELLOW}{temperatura}°C")
            print(Fore.CYAN + f"☀️  Clima: {Fore.GREEN}{clima}")

            outfit_elegido = mostrar_recomendaciones_y_seleccionar(manager, estilo, ocasion, clima)
            
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
        plt.close('all')

if __name__ == "__main__":
    main()
