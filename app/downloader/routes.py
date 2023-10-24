from flask import render_template, request, send_file, session
import pytube
from app import app  # Importa la instancia de Flask desde el archivo principal
import os, re
from moviepy.editor import VideoFileClip

app.secret_key = 'your_secret_key_1284732472'

# Pasar el nombre de la aplicación y la URL de la imagen a la plantilla
app_descripcion = "Descarga vídeos de YouTube de forma rápida y sencilla en calidad HD"
app_image_url = "static/assets/images/youtube-downloader.png"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube-url']
        download_option = request.form.get('download-option')

        try:
            video = pytube.YouTube(youtube_url)
            original_title = video.title# Obtener el título original
            session['title'] = original_title  #Almacena el titulo en una variable de la sesion del usuario para luego utilarlo en html
            session['thumbnail-url'] = video.thumbnail_url
            # Limpiar el título del video para evitar caracteres no deseados
            cleaned_title = re.sub(r'[?/\\:*"<>|]', '_', original_title)

            if download_option == 'video':
                video_streams = video.streams.filter(progressive=True, file_extension="mp4").all()
                if video_streams:
                    video_stream = video_streams[-1]  # Choose the highest quality video stream
                    video_assets_folder = os.path.join(app.root_path, 'static', 'assets', 'videos')
                    video_stream.download(output_path=video_assets_folder, filename=f'{cleaned_title}.mp4')
            if download_option == 'audio':
                audio_stream = video.streams.filter(progressive=True, file_extension="mp4").first()
                if audio_stream:
                    # Define la carpeta de destino para el archivo MP3
                    assets_folder = os.path.join(app.root_path, 'static', 'assets', 'audio')
                    mp3_file_path = os.path.join(assets_folder, f'{video.title}.mp3')

                    # Descarga el archivo de audio MP4
                    audio_stream.download(output_path=assets_folder, filename=f'{cleaned_title}.mp4')

                    # Convierte el archivo MP4 a MP3 (requiere moviepy)
                    try:
                        video_clip = VideoFileClip(os.path.join(assets_folder, f'{cleaned_title}.mp4'))
                        audio_clip = video_clip.audio
                        audio_clip.write_audiofile(mp3_file_path)
                        audio_clip.close()
                        video_clip.close()

                        # Elimina el archivo MP4 original
                        os.remove(os.path.join(assets_folder, f'{video.title}.mp4'))


                    except Exception as e:
                        return f"Error durante la conversión a MP3: {str(e)}"
       

        except Exception as e:
            return f"Ocurrió un error: {str(e)}"

    # Limpiar la miniatura y el título cuando la página se carga por primera vez
    if request.method == 'GET':
        session['title'] = None
        session['thumbnail-url'] = None

    return render_template('youtube_downloader.html', app_image_url=app_image_url, app_descripcion=app_descripcion)


@app.route('/download/<filename>')
def download_video(filename):
    video_assets_folder = os.path.join(app.root_path, 'static', 'assets', 'videos')
    video_file_path = os.path.join(video_assets_folder, filename)

    try:
        # Envía el archivo para que se descargue en el navegador
        return send_file(video_file_path, as_attachment=True)
    except Exception as e:
        return f"Error al descargar el archivo: {str(e)}"


@app.route('/download-audio/<audio_filename>')
def download_audio(audio_filename):
    audio_assets_folder = os.path.join(app.root_path, 'static', 'assets', 'audio')
    audio_file_path = os.path.join(audio_assets_folder, audio_filename)

    try:
        # Envía el archivo para que se descargue en el navegador
        return send_file(audio_file_path, as_attachment=True)
    except Exception as e:
        return f"Error al descargar el archivo: {str(e)}"