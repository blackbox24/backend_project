FROM python:3.12-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app

COPY . .

RUN python -m pip install --no-cache-dir -r ./requirements.txt \
    && sed -i 's/\r$//g' /usr/src/app/entrypoint.sh \
    && chmod +x /usr/src/app/entrypoint.sh 

EXPOSE 8000

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]