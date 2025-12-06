# Build stage

FROM python:3.12-slim AS builder
WORKDIR /weather_app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime stage

FROM python:3.12-slim

WORKDIR /weather_app

COPY --from=builder /install /usr/local
COPY /weatherApp/ /weather_app/

EXPOSE 5000
ENV FLASK_APP=app.py

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:weather_app"]
