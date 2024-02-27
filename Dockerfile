FROM python:3.8.16-alpine

RUN apk add --no-cache socat

RUN addgroup -S spid3r1337 && adduser -S spid3r1337 -G spid3r1337
WORKDIR /home/spid3r1337

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./server.py .
COPY ./worker.py .
COPY ./server.py .
COPY ./result.txt .

CMD socat -T 30 -d -d TCP-LISTEN:9999,reuseaddr,fork EXEC:"python3 server.py"