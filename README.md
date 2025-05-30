# Proyecto 2 | Algoritmos y Estructuras de Datos
## Sistema de Recomendaciones de Outfits

Este proyecto proporciona recomendaciones personalizadas de outfits según el estilo, el clima actual y la ocasión.

---

## Características principales

- Registro e inicio de sesión con validación de contraseña segura.
- Detección automática del clima usando [wttr.in](https://wttr.in).
- Selección por estilo, ocasión y clima.
- Recomendaciones personalizadas desde Neo4j.
- Posibilidad de recibir sugerencias similares al outfit favorito.

---

## Requisitos

### Software

- **Python** 3.10 o superior
- **pip** (gestor de paquetes de Python)
- Conexión a internet activa para acceder a la API de clima  

### Requisitos de hardware mínimos

- 4 GB de RAM (recomendado)  
- Espacio en disco: mínimo 500 MB para instalación y datos  
- Sistema operativo: Windows, Linux o macOS compatible con Python 3.10+  

---

## Instalación

### 1. Clonar el repositorio (opcional)

```bash
git clone https://github.com/Diana-Sosa18/CC2016-PROYECTO2 
cd CC2016-PROYECTO2
```

### 2. Instalar dependencias de Python

Ejecuta los siguientes comandos para instalar las librerías necesarias:

```bash
pip install neo4j
pip install bcrypt
pip install requests
pip install python-dotenv
```

### 3. Configurar Neo4j

- Configura las credenciales (URI, usuario y contraseña) en el archivo `.env`.

---

## Uso del sistema

Para iniciar el programa, ejecuta:

```bash
python app.py
```

### Flujo básico

1. El sistema solicita registro o inicio de sesión.  
2. Tras autenticarse, el usuario selecciona su estilo preferido (Hipster, Elegante, Vintage).  
3. Se obtiene automáticamente el clima actual para ajustar las recomendaciones.  
4. El usuario selecciona la ocasión (fiesta, universidad o trabajo).  
5. Se muestran outfits recomendados según las opciones seleccionadas.  
6. El usuario elige su outfit favorito y puede pedir recomendaciones similares.  
7. Puede repetir la selección de estilo para nuevas recomendaciones o salir del programa.
