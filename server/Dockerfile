FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir -p /usr/src/enigma/server/
WORKDIR /usr/src/enigma/server/

COPY . .

RUN python3 -m pip install --upgrade pip && pip install --no-cache-dir -r ./requirements.txt