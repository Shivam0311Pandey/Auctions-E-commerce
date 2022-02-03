FROM python:3
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn auctions.wsgi:application --bind 0.0.0.0:$PORT
