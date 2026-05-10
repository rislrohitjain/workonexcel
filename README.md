Steps for setup the project on evnv and running


python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt



venv\Scripts\activate
uvicorn app_backend:app --reload --port 8000

venv\Scripts\activate
python app_frontend.py
