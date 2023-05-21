from flask import Flask
from flask import render_template
from flask import  request, jsonify
import txtToImg, textToVideo
import openai,config
import requests
import json
import time


app = Flask(__name__)

openai.api_key = config.OPENAI_API_KEY
messages = [{"role": "system", "content": 'You are a science teacher. You should always be kind even if user insulted or humiliated you. Use sentimental analysis. Respond to all inputs in English whatever the input language.'}]

character_image= "https://create-images-results.d-id.com/api_docs/assets/noelle.jpeg"
#prompt_msg = "Our solar system consists of our star, the Sun, and everything bound to it by gravity – the planets Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune; dwarf planets such as Pluto; dozens of moons; and millions of asteroids, comets, and meteoroids."
#prompt_msg = "Hello, How are you"

@app.route("/")
def hello_world():
    return render_template('course-details.html')

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
    
    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript = message['role'] + ": " + message['content'] + "<br/>"

    return jsonify({'transcription': chat_transcript})

@app.route('/txtToImg', methods=['POST'])
def createImgAPI():
    content = request.json 
    return txtToImg.createImg(content['transcript'])


def createVideo(prompt_msg):
  url = "https://api.d-id.com/talks"
  payload = {
    "script": {
    "type": "text",
    "input": prompt_msg
    },
   "source_url": character_image
     }

  response = requests.post(url, json=payload, headers={
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Basic {config.DID_API_KEY}"
  })
  print(response.text)
  videoId = json.loads(response.text)["id"]
  print(videoId)
  return videoId


#get the generated talk 

def getTalk(videoId):
    #delay
 time.sleep(5)
 
 url = "https://api.d-id.com/talks/"+videoId

 response = requests.get(url, headers={
    "accept": "application/json",
    "authorization": f"Basic {config.DID_API_KEY}"
 })

 status = json.loads(response.text)["status"]
 
 if status == 'done':
     videoURL = json.loads(response.text)["result_url"]
     return videoURL
 elif status == 'created':
     getTalk(videoId)
 else:
     print("somthing went wrong please try again!!")


@app.route('/videoTalk', methods=['POST'])
def videoTalk():
    content = request.json 
    videoId = createVideo(content['transcript'])
    videoURL = getTalk(videoId)
    return videoURL


@app.route("/textToVideo/<string:prompt>")
def createVideoAPI(prompt):
    print(prompt)
    # return video path
    return textToVideo.createVideo(prompt)

