FROM python:3.7-stretch
COPY requirements.txt /app/requirements.txt
RUN pip install -r app/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["python3","manage.py", "run"]
