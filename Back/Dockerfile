FROM python:alpine

# install cmake and git gcc g++ make
RUN apk add --no-cache make cmake git gcc g++

WORKDIR /app

RUN git clone https://github.com/PotatoSpudowski/fastLLaMa

WORKDIR /app/fastLLaMa

RUN pip install py-cpuinfo

RUN mkdir build

WORKDIR /app/fastLLaMa/build

RUN cmake ..

RUN make



WORKDIR /app/fastLLaMa

COPY main.py .
COPY entrypoint.sh .
#COPY ./models/7B/ggml-alpaca-7b-q4.bin models/7B/ggml-alpaca-7b-q4.bin

RUN pip install fastapi uvicorn[standard] 

ENTRYPOINT ["sh", "entrypoint.sh"]

