# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the rest of your application's code
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Define the command to run your application using Gunicorn
CMD ["gunicorn", "-b", "host.docker.internal:8000", "app:app"]
