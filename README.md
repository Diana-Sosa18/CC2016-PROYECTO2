# Proyecto 2 | Algoritmos y Estructuras de Datos

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
