# backend/app.py
from src.api.routes import app

if __name__ == '__main__':
    app.run(debug=True)