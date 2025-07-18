FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN python -m pip install --no-cache-dir -r ./requirements.txt \
    && python manage.py migrate \
    && python manage.py collectstatic \
    # && python manage.py seed_db \
    && python manage.py test

EXPOSE 8000

# CMD ["python","manage.py","runserver"]