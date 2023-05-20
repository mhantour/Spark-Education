#@title Setup pipeline
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
from IPython.display import HTML
import base64
import config
import imageio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# from skimage.transform import resize


def display_video(video):
    fig = plt.figure(figsize=(4.2,4.2))  #Display size specification
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    mov = []
    for i in range(len(video)):  #Append videos one by one to mov
        img = plt.imshow(video[i], animated=True)
        plt.axis('off')
        mov.append([img])
    #Animation creation
    anime = animation.ArtistAnimation(fig, mov, interval=100, repeat_delay=1000)
    plt.close()
    return anime

def createVideo(promptVar):
    pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float, variant="fp16")
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    if (config.USE_GPU == True):
        pipe.enable_model_cpu_offload()
        pipe.enable_vae_slicing()

    #@title Generate your video
    prompt = promptVar #@param {type:"string"}
    negative_prompt = 'low quality' #@param {type:"string"}
    video_duration_seconds = config.Video_Duration #@param {type:"integer"}
    num_frames = video_duration_seconds * 10

    video_frames = pipe(prompt, negative_prompt=negative_prompt, num_inference_steps=config.Video_Steps, num_frames=num_frames).frames
    video_path = export_to_video(video_frames)
    # video_path = "C:\\Users\\903590\\AppData\\Local\\Temp\\tmphyz2w1on.mp4"
    video = imageio.mimread(video_path)  #Loading video
    videoHtml = display_video(video)#.to_html5_video()  #Inline video display in HTML5

    return videoHtml.to_html5_video()   # return video_path
