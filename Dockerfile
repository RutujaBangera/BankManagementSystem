FROM python:3.9-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install gcc default-libmysqlclient-dev pkg-config -y

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
