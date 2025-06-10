# Python 3.11 rasmini ishlatamiz
FROM python:3.11-slim

# Ish katalogini belgilaymiz
WORKDIR /app

# Tizim paketlarini yangilaymiz va kerakli kutubxonalarni o'rnatamiz
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Requirements faylini nusxalaymiz va bog'liqliklarni o'rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Barcha loyiha fayllarini nusxalaymiz
COPY . .

# Port 8000ni ochib qo'yamiz
EXPOSE 8000

# FastAPI'ni ishga tushirish buyrug'i
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]