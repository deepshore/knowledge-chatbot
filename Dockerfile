FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
COPY app/main.py /app/
COPY storage/ /app/

RUN pip install -r requirements.txt

CMD uvicorn main:app --port 8080 --host 0.0.0.0