FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD uvicorn chatbot-api:app --port 8000 --host 0.0.0.0