FROM python:3.13.2-alpine
RUN apk add g++ 

WORKDIR /app

COPY requirements-server.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY common.py common.py
COPY server.py app.py
COPY settings.json .

ENV PYTHONUNBUFFERED 1
EXPOSE 5000/tcp

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-w", "1"]