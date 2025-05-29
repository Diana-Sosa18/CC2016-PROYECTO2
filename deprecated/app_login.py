from colorama import init, Fore, Back, Style
from models import UserManager

# Inicializar colorama
init(autoreset=True)

def show_menu():
    print("\n" + Fore.CYAN + "="*40)
    print(Fore.YELLOW + Style.BRIGHT + "🌟 SISTEMA DE RECOMENDACIÓN DE ESTILOS 🌟")
    print(Fore.CYAN + "="*40)
    print(Fore.GREEN + "\n1. 📝 Registrarse")
    print(Fore.GREEN + "2. 🔑 Iniciar sesión")
    print(Fore.GREEN + "3. 🚪 Salir")
    return input(Fore.MAGENTA + "\n👉 Selecciona una opción: ").strip()

def user_menu(manager, username):
    while True:
        print("\n" + Fore.CYAN + "="*40)
        print(Fore.YELLOW + Style.BRIGHT + f"👤 MENÚ DE {username.upper()} 👤")
        print(Fore.CYAN + "="*40)
        print(Fore.BLUE + "\n1. 👀 Ver mi estilo")
        print(Fore.BLUE + "2. ✏️ Cambiar estilo")
        print(Fore.BLUE + "3. 👗 Obtener recomendación")
        print(Fore.BLUE + "4. 🔒 Cerrar sesión")
        
        option = input(Fore.MAGENTA + "\n👉 Elige una opción: ").strip()
        
        if option == "1":
            manager.view_user_style(username)
        elif option == "2":
            manager.change_user_style(username)
        elif option == "3":
            manager.get_user_recommendation(username)
        elif option == "4":
            print(Fore.GREEN + "\n✅ Sesión cerrada correctamente")
            break
        else:
            print(Fore.RED + "\n❌ Opción no válida")
        
        input(Fore.CYAN + "\nPresiona Enter para continuar...")

def main():
    manager = UserManager()
    
    try:
        while True:
            option = show_menu()
            
            if option == "1":
                print("\n" + Fore.CYAN + "="*40)
                print(Fore.YELLOW + Style.BRIGHT + "📝 REGISTRO DE NUEVO USUARIO 📝")
                print(Fore.CYAN + "="*40)
                username = input(Fore.BLUE + "\nNombre de usuario: ").strip()
                password = input(Fore.BLUE + "Contraseña: ").strip()
                
                if not username or not password:
                    print(Fore.RED + "\n❌ Usuario y contraseña son obligatorios")
                    continue
                
                success, message = manager.register_user(username, password)
                print(Fore.GREEN + f"\n✅ {message}" if success else Fore.RED + f"\n❌ {message}")
            
            elif option == "2":
                print("\n" + Fore.CYAN + "="*40)
                print(Fore.YELLOW + Style.BRIGHT + "🔑 INICIO DE SESIÓN 🔑")
                print(Fore.CYAN + "="*40)
                username = input(Fore.BLUE + "\nUsuario: ").strip()
                password = input(Fore.BLUE + "Contraseña: ").strip()
                
                if manager.login(username, password):
                    print(Fore.GREEN + Style.BRIGHT + f"\n✨ ¡Bienvenid@ {username}! ✨")
                    user_menu(manager, username)
                else:
                    print(Fore.RED + "\n❌ Credenciales incorrectas")
            
            elif option == "3":
                print(Fore.YELLOW + Style.BRIGHT + "\n👋 ¡Hasta pronto! 👋")
                break
            
            else:
                print(Fore.RED + "\n❌ Opción no válida")
                input(Fore.CYAN + "Presione Enter para continuar...")
    
    finally:
        manager.close()

if __name__ == "__main__":
    main()