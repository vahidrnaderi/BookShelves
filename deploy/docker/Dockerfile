FROM python:3.9

ADD aap/ /opt/aap
WORKDIR /opt/aap
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD gunicorn aap.wsgi -b 0.0.0.0:8000