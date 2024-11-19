# Use the official Python image from the Docker Hub
FROM python:3.11-alpine AS builder

# Set environment variable to prevent python from writing pyc files
ENV PYTHONUNBUFFERED 1

# Create and set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to install dependencies
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app/

# Use gunicorn to serve the app
CMD ["gunicorn", "skyCarManager.wsgi:application", "--bind", "0.0.0.0:8000", "--env", "DJANGO_SETTINGS_MODULE=skyCarManager.settings.prod"]
