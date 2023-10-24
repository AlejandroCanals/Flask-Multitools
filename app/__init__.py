from flask import Flask
app = Flask(__name__)

from app.downloader import routes
from app.pdf_merger import routes
from app.background_remover import routes
from app.routes import limpiar_manualmente ,limpiar_carpetas
