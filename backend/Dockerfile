FROM python:3.8.10-slim

# Install system dependencies
RUN apt-get update \
  && apt-get -y install tesseract-ocr

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD uvicorn main:app --port=8000 --host=0.0.0.0
