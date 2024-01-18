FROM ubuntu:22.04

RUN apt-get update && apt-get install -y supervisor socat gcc && apt-get clean

RUN useradd -md /home/spid3r user

WORKDIR /home/spid3r

COPY result.txt /home/spid3r/result.txt
COPY test.c .

RUN chmod +x ./test 
RUN chmod 444 ./flag.txt

EXPOSE 1337

CMD socat -T 30 -d -d TCP-LISTEN:1337,reuseaddr,fork EXEC:"./test"
