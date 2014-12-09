gunicorn sparks.wsgi --log-file - &
python manage.py celery worker --loglevel=INFO -Q http -n worker1.%h -c 20 -P eventlet --time-limit=30 &
python manage.py celery worker --loglevel=INFO -Q celery -n worker2.%h -c 3 --beat --time-limit=30
