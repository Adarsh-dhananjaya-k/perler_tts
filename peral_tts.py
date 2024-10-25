import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(device)

model = ParlerTTSForConditionalGeneration.from_pretrained(
    "parler-tts/parler-tts-mini-v1"
).to(device)
tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")

prompt = "In the heart of a bustling city, where the sounds of honking cars and chattering crowds blend into a symphony of urban life, a young artist named Clara dreams of creating a mural that captures the essence of her vibrant surroundings, showcasing the beauty of diversity and the stories of the people she encounters every day, from the elderly gentleman feeding pigeons in the park to the children playing joyfully on the streets, all while hoping to inspire others to appreciate the little moments that make life extraordinary and remind everyone that art has the power to unite us all. Feel free to use this sentence for your TTS testing!"
description = "A female indian teacher speaker delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up."

input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
audio_arr = generation.cpu().numpy().squeeze()
sf.write("parler_tts_out3.wav", audio_arr, model.config.sampling_rate)
