from flask import Flask, request, jsonify, send_file, send_from_directory
import yt_dlp
import os

app = Flask(__name__, static_folder="../Frontend/static", template_folder="../Frontend")

# Directorio donde se guardarán los archivos descargados
DOWNLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), "downloads")

# Asegúrate de que el directorio de descargas exista
if not os.path.exists(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)

# Ruta para servir el archivo HTML
@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'index.html')

# Ruta para manejar la descarga de videos
@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_DIRECTORY, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(result)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
