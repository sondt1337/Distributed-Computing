FROM python:3.8.16-alpine

RUN apt-get update \
    && apk add socat \
    && apt-get clean \*

# RUN useradd -md /home/spid3r user
RUN addgroup -S Spid3r && adduser -S Spid3r -G Spid3r

WORKDIR /home/spid3r

COPY ./server.py .
COPY result.txt /home/spid3r/result.txt
COPY ./worker.py .

RUN chmod 444 ./result.txt

EXPOSE 1337

CMD socat -T 30 -d -d TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 server.py"