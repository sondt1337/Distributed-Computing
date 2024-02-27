FROM python:3.8.16-alpine

RUN apk add --no-cache socat build-base libffi-dev openssl-dev python3-dev
RUN /usr/local/bin/python -m pip install --upgrade pip

RUN addgroup -S spid3r1337 && adduser -S spid3r1337 -G spid3r1337
WORKDIR /home/spid3r1337

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./server.py .
COPY ./worker.py .
COPY ./total.txt .
COPY ./result.txt .

CMD socat -T 30 -d -d TCP-LISTEN:9999,reuseaddr,fork EXEC:"python3 server.py"