FROM python:3.8.0-slim-buster

WORKDIR /ebook_automation

# https://github.com/geerlingguy/ansible-role-java/issues/64#issuecomment-393299088
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && \
    apt-get install -y pdftk exiftool

RUN rm -rf /var/cache/apt/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

COPY ./src/ ./

ENV COVER_PAGE=0
ENV COPYRIGHT_PAGE=4

CMD python main.py ./pdf_file.pdf ./output ./pdf_file.json