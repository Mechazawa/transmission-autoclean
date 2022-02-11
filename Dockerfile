FROM python:3

ENV SECURE false
ENV USERNAME ""
ENV PASSWORD ""
ENV HOST "127.0.0.1"
ENV PORT "9091"
ENV PATH "/transmission/"
ENV TIMEOUT 30
ENV DELETE false
ENV INTERVAL 30
ENV DEBUG false

RUN mkdir /app

COPY main.py /app/
COPY requirements.txt /app/

WORKDIR /app

RUN pip3 install --requirements requirements.txt

ENTRYPOINY ['python3', 'main.py']