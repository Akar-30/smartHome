from flask import Flask, render_template, request, jsonify # type: ignore
import assemblyai as aai
import os
from dotenv import load_dotenv # type: ignore

app = Flask(__name__)

load_dotenv()
aai.settings.api_key = os.getenv('ASSEMBLY_API')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    file_path = os.path.join('uploads', audio_file.filename)
    audio_file.save(file_path)

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)

    if transcript.status == aai.TranscriptStatus.error:
        return jsonify({'error': transcript.error}), 500
    else:
        return jsonify({'transcription': transcript.text})

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)