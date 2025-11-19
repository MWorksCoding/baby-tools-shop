# ===============================
# 1. Base image
# ===============================
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ===============================
# 2. Set work directory
# ===============================
WORKDIR /app

# ===============================
# 3. Install system dependencies
# ===============================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# 4. Install Python dependencies
# ===============================
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ===============================
# 5. Copy project files
# ===============================
COPY . ${WORKDIR}

# ===============================
# 6. Collect static files
# ===============================
RUN python manage.py collectstatic --noinput

# ===============================
# 7. Create non-root user
# ===============================
RUN adduser --disabled-password --no-create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

# ===============================
# 8. Expose port
# ===============================
EXPOSE 8025

# ===============================
# 9. Default command
# ===============================
# Runs migrations, then starts Gunicorn server
CMD ["sh", "-c", "python manage.py migrate && gunicorn babyshop.wsgi:application --bind 0.0.0.0:8025"]
