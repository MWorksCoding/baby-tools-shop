# Baby Tools Shop in Docker

This project is a **Django web application** packaged in a **Docker container** for easy deployment and portability.  
The instructions below explain how to build, run, and deploy the app on a **V-Server**, and how to access it via your server’s IP address and port.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#-quick-start)
3. [Usage](#-usage)
   - [Create a Docker Container](#-create-a-docker-container)
   - [Docker Management Commands](#-docker-management-commands)
4. [Project Checklist](#project-checklist)


## Prerequisites

Before you begin, ensure that the following are installed and set up on your local machine or server:
- [Docker](https://docs.docker.com/get-docker/)

## 🚀 Quick Start

Clone this repository and follow the setup instructions below to get the application running.

Open your command line and type the following commands:
With SSH configured (if SSH Keys are provided to GitHub)
```
git clone git@github.com:MWorksCoding/baby-tools-shop.git
```
Classic HTTPS (if no SSH Keys are provided to GitHub)
```
git clone https://github.com/MWorksCoding/baby-tools-shop.git
```

Create you virtual environment in your project directory with:
```
python -m venv venv
```

Activate your venv on Mac / Linux:
```
source venv/bin/activate
```

Activate your venv on Windows:
```
.\venv\Scripts\activate
```

Install dependencies:
```
pip install -r requirements.txt
```

Inside your project root, create a .env file with your environment variables:
```
touch .env
```

Set environment variables:
```
nano .env
```

Add your configuration variables, check [example.env] :
```
SECRET_KEY=<your_django_secret_key_from_setting.py>
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,<ip_server_address>
```

Navigate to the Django app directory:
```
baby-tools-shop/babyshop_app
```

Build the docker image: 

```
docker build -t babyshop_app .
```

Run the docker container on port 8025:
```
docker run -d -p 8025:8025 --env-file .env babyshop_app                                     
```

Open the container in your browser by visiting http://<ip_server_address>:8025

To add products to the Baby Tools Shop, you need access to the Django Admin Panel, which requires a superuser account.
First of all you need to find out the running Docker Container ID

```
docker ps
```

Then you paste this container id here to access the docker container and create a superuser
```
docker exec -it <container_id_or_name> python manage.py createsuperuser
```

You need to enter a username, a email address and a password.
After that you need to log in as superuser credentials under http://<ip_server_address>:8025/admin

Here you can add some categories, add products and manage existing entries.

## 🧑‍💻 Usage

### 🐳 Create a Docker Container

To containerize your Django project, create a file named [Dockerfile](babyshop_app/Dockerfile) in the same directory as your `manage.py` file. A Dockerfile is a text-based document with one purpose: creating a container image. It provides instructions to the image builder on the commands to run, files to copy, startup command, and more.

To reduce image size and improve build performance, create a [.dockerignore](babyshop_app/.dockerignore) file.

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

- [Download the Checklist](../baby-tools-shop/docs/checklist.pdf)