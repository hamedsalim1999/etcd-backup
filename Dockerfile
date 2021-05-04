FROM python:3.7

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "run.py"]