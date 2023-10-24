from flask import Flask

app = Flask(__name__)  # Crea una instancia de Flask para la aplicación downloader

# Configuración específica de la aplicación downloader
app.secret_key = 'your_secret_key_1284732472'
app.static_folder = "static"

# Importa y registra las rutas y vistas específicas de la aplicación downloader
from . import routes