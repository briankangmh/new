release: python manage.py migrate --noinput
web: daphne -p $PORT config.asgi:application -b 0.0.0.0