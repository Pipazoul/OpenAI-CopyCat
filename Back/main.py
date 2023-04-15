import json
import argparse

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import traceback
from llama_cpp import Llama


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = Llama(model_path="models/7B/qunt4_0.bin")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.websocket("/generate")
async def generate_text(websocket: WebSocket, num_tokens: int = 200, top_p: float = 0.85, temp: float = 0.7, repetition_p: float = 1.0, stop_word: str = "HUMAN:"):
    await websocket.accept()
    log_file = open("model_error.log", "a")
    
    # get websocket text message
    data = await websocket.receive_text()
    print("Received: {}".format(data))
    text = json.loads(data)["text"]
    params = json.loads(data)["params"]
    temp = json.loads(params)["temperature"]
    top_p = json.loads(params)["top_p"]
    repetition_p = json.loads(params)["repetition_p"]
    num_tokens = json.loads(params)["num_tokens"]
    stop_word = json.loads(params)["stop_word"]
    # convert stop word to list
    stop_word = stop_word.split(",")

    # print text length
    print("Text length: {}".format(len(text)))

    # if text length is greater than 800, truncate the older sentences 
    if len(text) > 800:
        text = text[-400:]
    


    async def generate(text, num_tokens=num_tokens, top_p=top_p, temp=temp, repetition_p=repetition_p, stop_word=stop_word):
        try:
            
            print("Generating...")
            print("Text: {}".format(text))
            print("Num tokens: {}".format(num_tokens))
            print("Top p: {}".format(top_p))
            print("Temp: {}".format(temp))
            print("Repetition penalty: {}".format(repetition_p))
            print("Stop word: {}".format(stop_word))
            stream = llm(
                text,
                max_tokens=num_tokens,
                #top_p=top_p,
                #temperature=temp,
                stop=stop_word,
                stream=True,
            )
            for output in stream:
                #print(json.dumps(output, indent=2))
                await websocket.send_text(output["choices"][0]["text"])
                
        except Exception as e:
            log_file.write("Error: {}\n".format(e))
            log_file.write("Traceback:\n")
            traceback.print_exc(file=log_file)
            print("Error: {}".format(e))

    await generate(text)
