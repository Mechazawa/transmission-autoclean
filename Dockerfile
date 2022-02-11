FROM python:3

RUN mkdir /app

COPY main.py /app/
COPY requirements.txt /app/

WORKDIR /app

RUN pip3 install --requirements requirements.txt

ENTRYPOINY ['python3', 'main.py']