release: python manage.py migrate --noinput && python manage collectstatic --no-input
web: gunicorn isitbinday.wsgi
