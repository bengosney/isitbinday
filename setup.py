#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='isitbinday',
      version='1.0',
      packages=find_packages(),
      scripts=['manage.py'],
      install_requires=[
          'django',
          'django-admin-sortable2',
          'django-appconf',
          'django-cors-headers',
          'django-fsm',
          'django-fsm-admin',
          'django-fsm-log',
          'django-heroku',
          'django-oso',
          'djangorestframework',
          'djangorestframework-simplejwt', 
          'googletrans',
          'rollbar',
          'openfoodfacts',
          'recurrent',
          ],
      )
