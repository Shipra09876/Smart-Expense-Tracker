# -------------------------------
# Dockerfile for Smart Expense Tracker Backend
# -------------------------------

# 1️⃣ Use official Python image
FROM python:3.11-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Copy requirements first (for caching)
COPY requirements.txt .

# 4️⃣ Install system dependencies (PostgreSQL client, build tools)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# 5️⃣ Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6️⃣ Copy entire project to container
COPY . .

# 7️⃣ Expose the port Django runs on
EXPOSE 8000

# 8️⃣ Default command to run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
