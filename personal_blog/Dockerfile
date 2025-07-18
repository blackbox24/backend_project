FROM python:3.12-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app

COPY . .

RUN python -m pip install --no-cache-dir -r ./requirements.txt \
    && python manage.py migrate \
    && python manage.py collectstatic \
    && python manage.py seed_db \
    && python manage.py test

EXPOSE 8000

# CMD ["python","manage.py","runserver"]