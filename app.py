from flask import Flask
from flask import render_template
from flask import  request, jsonify
import openai,config

openai.api_key = config.OPENAI_API_KEY
messages = [{"role": "system", "content": 'You are a helper teacher. Respond to all input in English.'}]

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('record-webrtc.html')

@app.route('/transcribe', methods=['GET'])
def transcribeGet():
    return "Hello";

@app.route('/transcribe', methods=['POST'])
def transcribe():
    global messages
    
    audio_blob = request.files['audio']
    audio_data = audio_blob.read()
    temp = './audio.wav'
    with open(temp, 'wb') as f:
        f.write(audio_data)
    audio_file= open(temp, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    
    messages.append({"role": "user", "content": transcript["text"]})
    
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "<br/>"

    return jsonify({'transcription': chat_transcript})

