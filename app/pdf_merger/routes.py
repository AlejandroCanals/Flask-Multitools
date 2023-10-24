from flask import render_template, request, send_file, flash, redirect, url_for
from app import app
import PyPDF2
import tempfile
import os

app.secret_key = 'your_secret_key_1284732472'
app_image_url = "static/assets/images/unir-pdf.png"
app_descripcion = " Combina múltiples documentos en formato PDF en un único archivo."


@app.route('/pdf-merger', methods=['GET', 'POST'])
def pdf_merger():
    if request.method == 'POST':
        pdf_files = request.files.getlist('pdf-files')

        if len(pdf_files) < 2:
            flash('Por favor, cargue al menos dos archivos PDF para fusionar.', 'warning')
            return redirect(url_for('pdf_merger'))

        pdf_final = PyPDF2.PdfMerger()
        for pdf_file in pdf_files:
            pdf_final.append(pdf_file)

        output_pdf = os.path.join(tempfile.gettempdir(), "output.pdf")
        pdf_final.write(output_pdf)
        pdf_final.close()

        return send_file(output_pdf, as_attachment=True)

    return render_template('pdf_merger.html', app_image_url=app_image_url,app_descripcion=app_descripcion)
