from app import app
from flask import render_template, request, flash, redirect, url_for,send_file,session
import os, io
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename

app_image_url = "static/assets/images/removebg.jpg"
app_descripcion = "Elimina el fondo de tu imagen"
app.config['UPLOAD_FOLDER'] = os.path.abspath('app/static/assets/uploads')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def remove_background(image):
    image_byte = io.BytesIO()
    image = image.convert("RGB")
    image.save(image_byte, format="PNG")
    image_byte.seek(0)
    processed_image_bytes = remove(image_byte.read())
    return Image.open(io.BytesIO(processed_image_bytes))

def process_image(file):
    image = Image.open(file)
    processed_image = remove_background(image)
    return processed_image

@app.route('/background-remover', methods=['GET', 'POST'])
def background_template():
    processed_image_url = None  # Inicialmente, no hay imagen procesada

    if request.method == 'POST':
        if 'background-files' not in request.files:
            flash('No se seleccionó ningún archivo.')
        else:
            file = request.files['background-files']
            if file.filename == '':
                flash('No se seleccionó ningún archivo.')
            elif file:
                processed_image = process_image(file)
                processed_image_filename = secure_filename(file.filename)
                processed_image_filename = os.path.splitext(processed_image_filename)[0] + '.png'
                processed_image.save(os.path.join(app.config['UPLOAD_FOLDER'], processed_image_filename))
                print("Ruta del archivo guardado:", os.path.join(app.config['UPLOAD_FOLDER'], processed_image_filename))
                processed_image_url = os.path.join('static/assets/uploads', processed_image_filename)
                session['processed_image_filename'] = processed_image_filename

   

    return render_template('background_remover.html', app_image_url=app_image_url, app_descripcion=app_descripcion, processed_image_url=processed_image_url)


@app.route('/download-processed-image')
def download_processed_image():
    if 'processed_image_filename' in session:
        # Obtiene el nombre del archivo de imagen procesada de la sesión
        processed_image_filename = session['processed_image_filename']

        # Accede a la carpeta de imágenes procesadas
        assets_folder = os.path.join(app.root_path, 'static', 'assets', 'uploads')

        # Accede a la ruta del archivo de imagen procesada
        file_path = os.path.join(assets_folder, processed_image_filename)

        # Envía el archivo para que se descargue en el navegador
        return send_file(file_path, as_attachment=True)

    return redirect(url_for('index'))