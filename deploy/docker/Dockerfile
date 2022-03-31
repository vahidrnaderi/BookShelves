FROM python:3.9

ADD bookshelves/ /opt/bookshelves
WORKDIR /opt/bookshelves
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD gunicorn bookshelves.wsgi -b 0.0.0.0:8000