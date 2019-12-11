FROM python:3.8.0-slim-buster

WORKDIR /ebook_automation

RUN apt-get update && \
    apt-get install -y zip unzip epubcheck

RUN rm -rf /var/cache/apt/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY run ./
COPY ./src/ ./src/

CMD bash run epub_file
