from flask import Flask, render_template

from neo4j import GraphDatabase
from recommendation_manager import RecommendationManager
from db_connection import URI, USER, PASSWORD
from models import UserManager

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
        seleccion = input("👉 Ingresa el número del outfit que más te gusta (1-3): ")
        if seleccion in ["1", "2", "3"]:
            return recomendaciones[int(seleccion) - 1]
        print("❌ Selección inválida. Intenta de nuevo.")

def obtener_estilo_clima_de_outfit(manager, nombre_outfit):
    query = """
    MATCH (o:Outfit {Name: $name})-[:PERTENECE_A]->(s:Style),
          (o)-[:ADEQUADO_PARA]->(c:Climate)
    RETURN s.Name AS estilo, c.Name AS clima
    """
    with manager.driver.session() as session:
        result = session.run(query, {"name": nombre_outfit})
        record = result.single()
        if record:
            return record["estilo"], record["clima"]
        return None, None

def main():
    from models import UserManager

    print("👋 ¡Bienvenido al recomendador de outfits!\n")
    user_manager = UserManager()

    while True:
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Selecciona una opción (1, 2 o 3): ")

        if opcion == "1":
            username = input("Nombre de usuario: ")
            password = input("Contraseña: ")
            if user_manager.login(username, password):
                print(f"✅ ¡Bienvenido de nuevo, {username}!")
                break
            else:
                print("❌ Nombre de usuario o contraseña incorrectos.")
        elif opcion == "2":
            username = input("Elige un nombre de usuario: ")
            password = input("Crea una contraseña: ")
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

    # Conectar con Neo4j una vez
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    manager = RecommendationManager(driver)

    while True:
        estilos_disponibles = ["Hipster", "Elegante", "Vintage"]
        print("\n🎨 ¿Qué estilo prefieres hoy?")
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

        recomendaciones = mostrar_recomendaciones(estilo_elegido, clima_mapeado, manager)
        if not recomendaciones:
            continue  # Regresa a elegir estilo

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
                break  # Regresa a seleccionar estilo

            nuevos = manager.get_similar_recommendations(
                outfit_elegido["Name"], estilo_elegido, clima_mapeado, historial_nombres)

            if not nuevos:
                print("❌ No se encontraron más recomendaciones similares.")
                break  # Regresa a seleccionar estilo

            combinados = [outfit_elegido] + nuevos[:2]
            for i, outfit in enumerate(combinados, 1):
                print(f"\n🔹 Outfit {i}:")
                print(f"   - Nombre: {outfit['Name']}")
                print(f"   - Imagen ID: {outfit['ID_Image']}")

            outfit_elegido = elegir_outfit(combinados)
            historial_nombres.add(outfit_elegido["Name"])

    manager.close()
    user_manager.close()

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)