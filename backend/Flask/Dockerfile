FROM python:3.9

WORKDIR /app

COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

#CMD ["python", "/app/app.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
