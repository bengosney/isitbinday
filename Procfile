release: python manage.py migrate --noinput && python manage.py collectstatic --no-input
web: gunicorn isitbinday.wsgi
