FROM python:alpine

WORKDIR /app

RUN apk add cmake g++ make

RUN pip install llama-cpp-python

COPY main.py .
COPY entrypoint.sh .
#COPY ./models/7B/ggml-alpaca-7b-q4.bin models/7B/ggml-alpaca-7b-q4.bin

RUN pip install fastapi uvicorn[standard] 

ENTRYPOINT ["sh", "entrypoint.sh"]

