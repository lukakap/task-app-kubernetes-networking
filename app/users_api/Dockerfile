# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port on which the application will run
EXPOSE 8002

# Start the application
CMD ["uvicorn", "users_api:app", "--host", "0.0.0.0", "--port", "8002"]