from google.cloud import speech
import replicate
from scipy.io.wavfile import write
import io

client = speech.SpeechClient()
# model = replicate.models.get("openai/whisper")
# client = model.versions.get("089ea17a12d0b9fc2f81d620cc6e686de7a156007830789bf186392728ac25e8")

def transcribe_speech(content_buffer, fs, name, age, gender, hobbies, history):

    # Write int16 buffer to actual in-memory WAV file with headers
    f = io.BytesIO()
    write(f, fs, content_buffer)
    content = f.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
      encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
      sample_rate_hertz=fs,
      language_code="nl-BE",
      enable_automatic_punctuation=True,
      speech_contexts=[speech.SpeechContext(phrases=[name, "Sinterklaas", *hobbies])],
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:        
        return result.alternatives[0].transcript
    
    # hobbystring = hobbies.replace("[", "").replace("]", "").replace('"', '')
    # initial_prompt = f"{name} is een {gender} van {age} jaar oud die houdt van {hobbystring}. {history}"
    # output = client.predict(audio=f, model="medium", language="nl", initial_prompt=initial_prompt, condition_on_previous_text=True)
    # out = output['transcription'].replace("<|transcribe|>", "").strip()
    # if len(out) > 0:
    #     return out
    # else:
    #     return None
