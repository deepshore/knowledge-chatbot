FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt /app/
COPY app/main.py /app/
COPY storage/ /app/

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

CMD uvicorn main:app --port 8080 --host 0.0.0.0