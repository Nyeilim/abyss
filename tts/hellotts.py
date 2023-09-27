# https://huggingface.co/suno/bark-small
# https://github.com/suno-ai/bark
from transformers import AutoProcessor, AutoModel
import scipy
# from IPython.display import Audio

processor = AutoProcessor.from_pretrained("suno/bark-small")
model = AutoModel.from_pretrained("suno/bark-small")

inputs = processor(
    text=["Hello, my name is Suno. And, uh — and I like pizza. [laughs] But I also have other interests such as playing tic tac toe."],
    return_tensors="pt",
)

speech_values = model.generate(**inputs, do_sample=True)

# output .wav, need scipy module
sampling_rate = model.generation_config.sample_rate
scipy.io.wavfile.write("bark_out.wav", rate=sampling_rate, data=speech_values.cpu().numpy().squeeze())

# listen directly, need IPython module
# sampling_rate = model.generation_config.sample_rate
# Audio(speech_values.cpu().numpy().squeeze(), rate=sampling_rat