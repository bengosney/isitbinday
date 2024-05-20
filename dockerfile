FROM python:3.12

ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt


COPY . /app

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "isitbinday.wsgi:application", "--bind", "0.0.0.0:8000"]
