FROM python:3.13-slim

WORKDIR /app
    
RUN apt-get update && apt-get install -y python3-dev pkg-config default-libmysqlclient-dev build-essential

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
