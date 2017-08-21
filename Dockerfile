FROM python:3.6

EXPOSE 5001

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD gunicorn app:app -k aiohttp.worker.GunicornWebWorker -b 0.0.0.0:5001
