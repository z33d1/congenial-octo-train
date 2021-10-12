FROM python:3.7-stretch
COPY requirements.txt /app/requirements.txt
RUN pip install -r app/requirements.txt
COPY . /app
WORKDIR /app
RUN python3 manage.py setup_db
EXPOSE 8089
ENTRYPOINT ["python3","manage.py", "run"]
