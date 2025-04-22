FROM python:3.11

# Install git
RUN apt-get update && apt-get install -y git

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
