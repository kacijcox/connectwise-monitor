#!/bin/bash
gunicorn --config gunicorn.conf.py src.api.routes:app