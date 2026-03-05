#!/bin/bash

echo "Kutib turing: Ma'lumotlar bazasi (PostgreSQL) ishga tushmoqda..."
# Baza to'liq ishlashga tayyor bo'lishi uchun 10 soniya kutamiz
sleep 10

echo "1-qadam: CSV fayllarni bazaga yozish (load_to_db.py) ishga tushmoqda..."
python load_to_db.py

echo "2-qadam: FastAPI serveri ishga tushirilmoqda..."
uvicorn main:app --host 0.0.0.0 --port 8000