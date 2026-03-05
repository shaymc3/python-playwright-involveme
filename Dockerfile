# Use the official Microsoft Playwright image
FROM mcr.microsoft.com/playwright/python:v1.57.0-noble

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Environment variables (can be overridden by docker-compose)
ENV PYTHONUNBUFFERED=1

# Run tests by default (using allure-results directory)
CMD ["pytest", "--alluredir=allure-results"]
