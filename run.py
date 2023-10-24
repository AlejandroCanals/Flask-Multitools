from app import app  # Importa la instancia de Flask desde la aplicación principal

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501,debug=True)  # Ejecuta la aplicación en el servidor

