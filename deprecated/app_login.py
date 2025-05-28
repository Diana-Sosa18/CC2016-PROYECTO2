
from models import UserManager

def show_menu():
    print("\n" + "="*40)
    print("🌟 SISTEMA DE RECOMENDACIÓN DE ESTILOS")
    print("="*40)
    print("\n1. Registrarse")
    print("2. Iniciar sesión")
    print("3. Salir")
    return input("\n👉 Selecciona una opción: ").strip()

def user_menu(manager, username):
    while True:
        print("\n" + "="*40)
        print(f"👤 MENÚ DE {username.upper()}")
        print("="*40)
        print("\n1. Ver mi estilo")
        print("2. Cambiar estilo")
        print("3. Obtener recomendación")
        print("4. Cerrar sesión")
        
        option = input("\n👉 Elige una opción: ").strip()
        
        if option == "1":
            manager.view_user_style(username)
        elif option == "2":
            manager.change_user_style(username)
        elif option == "3":
            manager.get_user_recommendation(username)
        elif option == "4":
            print("\n✅ Sesión cerrada correctamente")
            break
        else:
            print("\n❌ Opción no válida")
        
        input("\nPresiona Enter para continuar...")

def main():
    manager = UserManager()
    
    try:
        while True:
            option = show_menu()
            
            if option == "1":
                print("\n" + "="*40)
                print("📝 REGISTRO DE NUEVO USUARIO")
                print("="*40)
                username = input("\nNombre de usuario: ").strip()
                password = input("Contraseña: ").strip()
                
                if not username or not password:
                    print("\n❌ Usuario y contraseña son obligatorios")
                    continue
                
                success, message = manager.register_user(username, password)
                print(f"\n{message}")
            
            elif option == "2":
                print("\n--- Inicio de sesión ---")
                username = input("Usuario: ").strip()
                password = input("Contraseña: ").strip()
                
                if manager.login(username, password):
                    print(f"\n¡Bienvenid@ {username}!")
                    
                else:
                    print("\nCredenciales incorrectas")
            
            elif option == "3":
                print("\n👋 ¡Hasta pronto!")
                break
            
            else:
                print("\nOpcion no válida")
                input("Presione Enter para continuar...")
    
    finally:
        manager.close()

if __name__ == "__main__":
    main()
