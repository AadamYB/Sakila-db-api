FROM python:3.12-slim

WORKDIR /app
    
RUN apt-get update && apt-get install -y python3-dev pkg-config default-libmysqlclient-dev build-essential

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . .

EXPOSE 8000

RUN echo "Printing pip-installed Flask: " && python3 -m pip list | grep Flask && sleep 9

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
