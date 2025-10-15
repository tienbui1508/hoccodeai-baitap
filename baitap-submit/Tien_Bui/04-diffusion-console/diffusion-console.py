from diffusers import DiffusionPipeline, EulerDiscreteScheduler, DDIMScheduler, DPMSolverMultistepScheduler
import torch

pipeline = DiffusionPipeline.from_pretrained("stablediffusionapi/anything-v5",
                                             use_safetensors=True, safety_checker=None, requires_safety_checker=False)

device = "cuda" if torch.cuda.is_available() else "cpu"
pipeline.to(device)

prompt = input("Enter your prompt: ")
height =int(input("Enter image height: "))
width = int(input("Enter image width: "))

height = round(height / 8) * 8
width = round(width / 8) * 8

image = pipeline(
    prompt,
    height=height,
    width=width,
    guidance_scale=7,
    num_inference_steps=20,
    negative_prompt="ugly, deformed, disfigured, low quality, worst quality",
    generator=torch.Generator(device=device).manual_seed(42),
).images[0]
image.show()
image.save("bai4.png")
