# Basic Dockerfile for running the app in a container for testing
# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable for config file
ENV MULTI_GIT_CONFIG /app/config.py

# Run run.py when the container launches
CMD ["python", "run.py"]
