FROM python:3.11.2

WORKDIR home

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py viz.py datasets.py app.py .

COPY assets assets

ENTRYPOINT python main.py
