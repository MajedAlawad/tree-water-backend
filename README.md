
# Tree Water Backend (Production Ready)

Flask-based API for estimating water needs for tree species in Saudi Arabia.

## Endpoints

- `/` – Simple HTML form
- `/trees` – List all tree species
- `/calculate` – POST to calculate water consumption

## Local Run
```bash
pip install -r requirements.txt
python app.py
```

## Production (Gunicorn)
```bash
gunicorn -b 0.0.0.0:10000 app:app
```
