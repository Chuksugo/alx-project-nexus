FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app

RUN adduser --disabled-password --gecos "" webuser || true
RUN chown -R webuser:webuser /app
USER webuser

EXPOSE 8000

CMD ["gunicorn", "alx_project_nexus.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
