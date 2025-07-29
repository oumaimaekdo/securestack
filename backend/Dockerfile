FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y gcc libpq-dev netcat-openbsd postgresql-client && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x wait_for_db.sh

EXPOSE 8000

CMD ["./wait_for_db.sh", "sh", "-c", "python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:8000"]

