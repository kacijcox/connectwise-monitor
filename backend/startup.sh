# backend/startup.sh
#!/bin/bash
cd /home/site/wwwroot
gunicorn --bind=0.0.0.0:8000 "src.api.routes:app" &
python monitor.py

