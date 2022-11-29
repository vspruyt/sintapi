from fastapi import FastAPI, Form, File, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scipy.io.wavfile import write
import numpy as np

from typing import List

import speech2text
import sinterklaasbot
import text2speech

app = FastAPI()

origins = [    
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process_audio/")
def process_audio(audio: bytes=File(), sequence_id: int=Form(), name: str=Form(), age: int=Form(), gender: str=Form(), hobbies: str=Form(), history: str=Form()):
    audio_pcm = np.frombuffer(audio, dtype='int16')
    # with open('test.wav', 'wb+') as f:
    #     write(f, 16000, audio_pcm)
    transcription = speech2text.transcribe_speech(audio_pcm, 16000, name, age, gender, hobbies, history)
    return {"sequence_id": sequence_id, "text": transcription}

class SpeakerModel(BaseModel):
    name: str
    age: int
    hobbies: List[str]
    gender: str
    history: List[str]

@app.post("/generate_response/")
def generate_response(input: SpeakerModel):    
    nr_trials = 0
    resp = None
    while nr_trials < 3:
        resp = sinterklaasbot.get_response(input.name, input.gender, input.age, input.hobbies, input.history)
        if resp is not None:
            resp = resp.strip()
            if len(resp) > 0:
                break
        nr_trials += 1

    return {"text": resp}


@app.post("/generate_audio/")
def generate_audio(text:str = Body(..., embed=True)):    
    res = text2speech.generate_audio(text)
    return Response(content=res, media_type="audio/mpeg")

