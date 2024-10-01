# Use an official Python runtime as a base image
FROM python:3.12.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code


# # Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install --default-timeout=120 -r requirements.txt

# Copy the rest of the project files to the container
COPY . /code/
