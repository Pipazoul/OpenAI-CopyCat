from typing import List
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import sys
import asyncio
sys.path.append("./build/")
import fastLlama
import threading
import queue
import traceback


MODEL_PATH = "models/7B/ggml-alpaca-7b-q4.bin"

model = fastLlama.Model(
        id="LLAMA-7B",
        path=MODEL_PATH, #path to model
        num_threads=8, #number of threads to use
        n_ctx=1024, #context size of model
        last_n_size=64, #size of last n tokens (used for repetition penalty) (Optional)
        seed=0 #seed for random number generator (Optional)
    )

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.websocket("/generate")
async def generate_text(websocket: WebSocket):
    await websocket.accept()

    text = await websocket.receive_text()

    # Define a queue to store the generated tokens
    token_queue = queue.Queue()

    # Define a log file to store any errors that occur in the model thread
    log_file = open("model_error.log", "a")

    def stream_token(x: str) -> None:
        """
        This function is called by the llama library to stream tokens
        """
        token_queue.put(x)

    # Define a function to run the model in a separate thread
    def generate(text):
        try:
            res = model.ingest(text)

            model.generate(
                num_tokens=200, 
                top_p=0.85, #top p sampling (Optional)
                temp=0.7, #temperature (Optional)
                repeat_penalty=1.0, #repetition penalty (Optional)
                streaming_fn=stream_token, #function to stream tokens (Optional)
                stop_word=["HUMAN:"] #stop generation when this word is encountered (Optional)
            )
        except Exception as e:
            # Write the error message and traceback to the log file
            log_file.write("Error: {}\n".format(e))
            log_file.write("Traceback:\n")
            traceback.print_exc(file=log_file)
            print("Error: {}".format(e))

            # Restart the model thread
            generate(text)

    # Start the model in a separate thread 
    try: 
        model_thread = threading.Thread(target=generate, args=(text,))
        model_thread.start()
    except Exception as e:
        # Write the error message to the WebSocket and the log file
        error_message = "Error: {}".format(e)
        log_file.write(error_message)
        print(error_message)
        await websocket.send_text(error_message)

    # Stream the generated tokens via the WebSocket
    while True:
        try:
            token = token_queue.get(block=False)
            await websocket.send_text(token)
        except queue.Empty:
            # If there are no more tokens in the queue, check if
            # the model thread is still running
            if not model_thread.is_alive():
                break
            else:
                # If the model thread is still running, wait 0.1 seconds
                # before checking the queue again
                await asyncio.sleep(0.1)
