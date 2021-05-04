FROM python:3.7
COPY . /app
WORKDIR app
RUN pip install -r requirements.txt
EXPOSE 2379
CMD ["python", "run.py"]