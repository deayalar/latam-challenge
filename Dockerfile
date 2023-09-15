# syntax=docker/dockerfile:1.2
FROM python:3.10-slim
# put you docker configuration here

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./ /code

CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8081"]

# commands
# docker build -t latam .
# docker run -d --name latam -p 8081:8081 latam