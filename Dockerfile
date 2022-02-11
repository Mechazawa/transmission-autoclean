FROM python:3

ENV SECURE false
ENV USERNAME ""
ENV PASSWORD ""
ENV HOST "127.0.0.1"
ENV PORT "9091"
ENV URL_PATH "/transmission/"
ENV TIMEOUT 30
ENV DELETE false
ENV INTERVAL 30
ENV DEBUG false

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ['python3', 'main.py']