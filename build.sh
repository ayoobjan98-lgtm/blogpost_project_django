pip install -r requirements.txt

python manage.py collectstatic
gunicorn blogpost.wsgi:application