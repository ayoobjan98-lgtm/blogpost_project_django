pip install -r requirements.txt

python manage.py collectstatic --noinput
gunicorn blogpost.wsgi:application