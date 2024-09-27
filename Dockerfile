# Use an official Python runtime as a base image
FROM python:3.12.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the requirements.txt file to the container
COPY requirements.txt /code/

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install --default-timeout=120 -r requirements.txt

# Copy the rest of the project files to the container
COPY . /code/

# Expose port 8000 for the Django app
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
