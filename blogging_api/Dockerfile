FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

RUN mkdir -p /app/staticfiles && \
    python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    mkdir -p /home/www/staticfiles && \
    cp -r /app/staticfiles/* /home/www/staticfiles/

EXPOSE 8000