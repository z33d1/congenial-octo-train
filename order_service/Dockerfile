FROM python:3.7-stretch
COPY . /app
WORKDIR /app
EXPOSE 8083
RUN pip install -r requirements.txt
ENTRYPOINT ["python3","manage.py", "run"]
