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

### Dependencias de Python

Para instalar las dependencias necesarias para el correcto funcionamiento del sistema, se deben ejecutar los siguientes comandos:

```bash
pip install neo4j
pip install python-dotenv
pip install bcrypt
python -m pip install requests
pip install pytest pytest-flask