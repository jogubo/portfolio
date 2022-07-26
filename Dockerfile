FROM python:3.10.5-alpine

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV FLASK_APP portfolio

ENV FLASK_ENV development

WORKDIR /usr/src/app

COPY . .

RUN pip install -e .

CMD flask init-db

ENTRYPOINT ["flask"] 

CMD ["run", "--host=0.0.0.0"] 
