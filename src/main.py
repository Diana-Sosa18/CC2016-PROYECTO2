from models import UserManager

def show_menu():
    print("\nBienvenido")
    print("1. Registrarse")
    print("2. Iniciar sesión")
    print("3. Salir")
    return input("Seleccione una opcion: ")

def main():
    manager = UserManager()
    
    try:
        while True:
            option = show_menu()
            
            if option == "1":
                print("\n--- Registro ---")
                username = input("Nombre de usuario: ").strip()
                password = input("Contraseña: ").strip()
                
                if not username or not password:
                    print("Error: Usuario y contraseña son obligatorios")
                    continue
                
                success, message = manager.register_user(username, password)
                print(message)
                if success:
                    input("\nPresione Enter para continuar...")
            
            elif option == "2":
                print("\n--- Inicio de sesion ---")
                username = input("Usuario: ").strip()
                password = input("Contraseña: ").strip()
                
                if manager.login(username, password):
                    print(f"\n¡Bienvenido {username}!")
                    
                else:
                    print("\nCredenciales incorrectas")
            
            elif option == "3":
                print("\n¡Hasta pronto!")
                break
            
            else:
                print("\nOpcion no válida")
    
    finally:
        manager.close()

main()