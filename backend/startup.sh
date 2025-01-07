cd /home/site/wwwroot
gunicorn --bind=0.0.0.0:8000 wsgi:app &  # Run web server
python scheduler.py                        # Run scheduler