FROM python:3.11.2

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py viz.py datasets.py app.py .

ENTRYPOINT python main.py
