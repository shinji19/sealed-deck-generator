FROM python:3.6.12

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
