FROM python:3.11-slim-bookworm

LABEL org.opencontainers.image.source = "https://github.com/deepshore/knowledge-chatbot"

WORKDIR /app

COPY requirements-all.txt /app/
COPY app/main.py /app/
COPY storage /app/storage

RUN python -m pip install --upgrade pip && \
    pip install -r requirements-all.txt

CMD uvicorn main:app --port 8080 --host 0.0.0.0