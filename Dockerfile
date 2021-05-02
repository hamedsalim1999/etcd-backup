FROM python:3.7

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /app

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]