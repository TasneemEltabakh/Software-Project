FROM python:3.12-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y pkg-config build-essential libmariadb-dev-compat libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask apps
CMD ["python", "app.py"]
