FROM python:3.11-slim

WORKDIR /app

# PostgreSQL bilan ishlash uchun kerakli tizim paketlari
RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*

# Talablarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani ko'chirish
COPY . .

# Skriptga ishga tushish huquqini berish
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]