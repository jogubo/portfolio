FROM python:3.10.5-alpine

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV FLASK_APP app.py

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src .

ENTRYPOINT ["flask"] 

CMD ["run", "--host=0.0.0.0"] 
