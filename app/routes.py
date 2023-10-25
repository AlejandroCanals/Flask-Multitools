import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from app import app

# Lista de carpetas que deseas limpiar
carpetas_a_limpiar = ['static/assets/videos', 'static/assets/audio', 'static/assets/uploads']

def limpiar_carpetas(carpetas_a_limpiar):
    for carpeta in carpetas_a_limpiar:
        ruta_carpeta = os.path.join(app.root_path, carpeta)
        if os.path.exists(ruta_carpeta):  # Verificar si la carpeta existe
            archivos_en_carpeta = os.listdir(ruta_carpeta)
            if archivos_en_carpeta:  # Verificar si hay archivos en la carpeta
                for archivo in archivos_en_carpeta:
                    ruta_archivo = os.path.join(ruta_carpeta, archivo)
                    os.remove(ruta_archivo)

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(limpiar_carpetas, 'interval', hours=1, args=[carpetas_a_limpiar])

if not scheduler.running:
    scheduler.start()

@app.route('/limpiar-manualmente')
def limpiar_manualmente():
    limpiar_carpetas(carpetas_a_limpiar)
    return "Limpieza manual de carpetas realizada."

