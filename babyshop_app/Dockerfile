# Django App in Docker

## Description
This project is a **Django web application** packaged in a **Docker container** for easy deployment and portability.  
The instructions below explain how to build, run, and deploy the app on a **V-Server**, and how to access it via your server’s IP address and port.

## Table of Contents

1. [Description](#description)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#-quick-start)
   - [Clone the Repository](#1-clone-the-repository)
   - [Set Up a Virtual Environment](#2-set-up-a-virtual-environment-linux--ubuntu)
   - [Install Dependencies](#3-install-dependencies)
   - [Configure Environment Variables](#4-configure-environment-variables)
   - [Run Migrations and Start the Server](#5-run-migrations-and-start-the-server)
4. [Usage](#-usage)
   - [Create a Docker Container](#-create-a-docker-container)
   - [Build and Run the Docker Container](#-build-and-run-the-docker-container)
   - [Docker Management Commands](#-docker-management-commands)
5. [Project Checklist](#project-checklist)


## Prerequisites

Before you begin, ensure that the following are installed and set up on your local machine or server:
- [Docker](https://docs.docker.com/get-docker/)
- A [GitHub](https://github.com/) account with SSH access configured (recommended)
- A V-Server (e.g., Ubuntu) with SSH access

## 🚀 Quick Start

Clone this repository and follow the setup instructions below to get the application running.

### 1. Clone the Repository

Open your command line and type the following commands:
With SSH configured (if SSH Keys are provided to GitHub)
```
git clone git@github.com:MWorksCoding/baby-tools-shop.git
```
Classic HTTPS (if no SSH Keys are provided to GitHub)
```
git clone https://github.com/MWorksCoding/baby-tools-shop.git
```

### 2. Set Up a Virtual Environment (Linux / Ubuntu)

Create you virtual environment (in your case it's Linux Ubuntu) in your project directory with:
```
    python -m venv venv
```

Activate your venv:
```
source venv/bin/activate
```
💡 Tip: To deactivate the environment, simply run deactivate.


### 3. Install Dependencies

Install dependencies:
```
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Inside your project root, create a .env file with your environment variables:
```
touch .env
```

Set environment variables:
```
nano .env
```

Add your configuration variables:
```
SECRET_KEY=<your_django_secret_key>
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,<ip_server_address>
```

### 5. Run Migrations and Start the Server

Navigate to the Django app directory:
```
cd baby-tools-shop/babyshop_app
```

Apply database migrations:
```
python manage.py migrate
```

Start the Django development server:
```
python manage.py runserver
```

Access the app in your browser:
```
http://localhost:8000
```

## 🧑‍💻 Usage

### 🐳 Create a Docker Container

To containerize your Django project, create a file named **`Dockerfile`** (without any extension) in the same directory as your `manage.py` file.  
Below is an example configuration tailored for this project:

In your Case it's: 

```
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
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# ===============================
# 5. Copy project files
# ===============================
COPY . /app/

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

```

To reduce image size and improve build performance, create a .dockerignore file in your project root directory with the following content:
```
venv/
__pycache__/
*.pyc
*.pyo
*.db
*.sqlite3
.env
.git
.gitignore
```

Before building your Docker image, make sure you have a requirements.txt file that lists all dependencies:
```
python -m pip freeze > requirements.txt
```

You should use a WSGI server such as Gunicorn for permanent deployments.

Gunicorn is a lightweight, production-grade web server that runs your Django app more efficiently and can handle multiple workers.
It acts as a **bridge** between your Python app and the outside world, efficiently handling multiple concurrent web requests.
Django’s built-in server (`python manage.py runserver`) is meant **only for development** — it’s single-threaded, slow, and not secure for production.

WhiteNoise helps Django handle static files (like CSS, JS, images) directly in production — safely and efficiently.

In development, Django serves static files automatically.
But in production, the default Django server doesn’t handle static files (for performance and security reasons).
Traditionally, this job is done by NGINX.
If you don’t want to set up NGINX or another web server just for static files, WhiteNoise solves this.

Gunicorn provides:

- **Multi-worker architecture** – handles many requests simultaneously  
- **Better performance** – optimized for speed and concurrency  
- **Production stability** – restarts gracefully if a worker crashes  
- **WSGI standard compliance** – works seamlessly with Django and NGINX

### 🐳 Build and Run the Docker Container

Navigate to the Django app directory:
```
baby-tools-shop/babyshop_app
```

1. Build the docker image: 

```
    docker build -t babyshop_app .
```

2. Run the docker container on port 8025:
```
    docker run -d -p 8025:8025 --env-file .env babyshop_app                                     
```

3. Open the container in your browser by visiting http://<ip_server_address>:8025


### 🧭 Docker Management Commands

List all images you’ve built or pulled
```
docker image ls
```

Remove specific images
```
docker rmi <docker_image_id>
```

See running containers:
```
docker ps
```

Stop running container:
```
docker stop <docker_container_id>
```

## Project Checklist

You can find a detailed checklist for this project in PDF format:

- [Download the Checklist](docs/checklist.pdf)