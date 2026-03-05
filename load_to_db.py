import pandas as pd
from sqlalchemy import create_engine

import os 


# Baza ulanish manzili (Format: postgresql://username:password@host:port/database_name)
# O'zingizning postgres parolingiz va baza nomingizni kiriting!
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'root')
DB_HOST = os.getenv('POSTGRES_HOST', 'db')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'business_db')

# --- POSTGRESQL ULANISH SOZLAMALARI ---
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def load_csv_to_postgres():
    print("Baza bilan aloqa o'rnatilmoqda...")
    engine = create_engine(DB_URL)
    
    # 1. CSV fayllarni o'qish
    print("CSV fayllar o'qilmoqda...")
    products_df = pd.read_csv('data/products.csv')
    sales_df = pd.read_csv('data/sales.csv')
    
    # 2. Bazaga yozish
    # if_exists='replace' -> agar jadval oldin bor bo'lsa, o'chirib yangidan yozadi
    # if_exists='append' -> oldingi ma'lumotlar ustiga qo'shib yozadi
    print("Ma'lumotlar PostgreSQL bazasiga yozilmoqda...")
    products_df.to_sql('products', engine, if_exists='replace', index=False)
    sales_df.to_sql('sales', engine, if_exists='replace', index=False)
    
    print("✅ Ma'lumotlar muvaffaqiyatli yuklandi!")

if __name__ == "__main__":
    load_csv_to_postgres()