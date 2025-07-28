FROM python:3.9-slim-buster

WORKDIR /myportfolio

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir
RUN pip3 install gunicorn

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

EXPOSE 5000