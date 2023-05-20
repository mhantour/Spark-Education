import base64
import os
import requests
import config

engine_id = "stable-diffusion-v1-5"
api_host = 'https://api.stability.ai'
api_key = config.STABILITY_API_KEY

def createImg(prompt):
    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "cfg_scale": 7,
            # "clip_guidance_preset": "FAST_BLUE",
            # "seed":11
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 30,
            "style_preset": "digital-art" #//"3d-model" //"photographic"
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    imgstring = data['artifacts'][0]['base64']
    img = '<img src="data:image/png;base64,'+imgstring+'">'
    return img