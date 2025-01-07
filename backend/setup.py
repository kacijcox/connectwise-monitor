# backend/setup.py
from setuptools import setup, find_packages

setup(
    name="connectwise-monitor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-cors',
        'gunicorn',
        'anthropic',
        'python-dotenv',
        'schedule'  # Added this for the scheduler functionality
    ]
)