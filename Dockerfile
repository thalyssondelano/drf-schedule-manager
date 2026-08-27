# Versão leve do Python.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# UV para maior velocidade de instalacao dos pacotes.
RUN pip install uv

COPY requirements.txt /app/
RUN uv pip install --system --no-cache -r requirements.txt

COPY . /app/