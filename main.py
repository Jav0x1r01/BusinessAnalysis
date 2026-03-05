from fastapi import FastAPI
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression # ML modelini qo'shdik
from typing import Literal

import os

app = FastAPI(title="Business Analytics API", version="1.1")


DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'root')
DB_HOST = os.getenv('POSTGRES_HOST', 'db')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'business_db')

# --- POSTGRESQL ULANISH SOZLAMALARI ---
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)

# --- MA'LUMOTLARNI BAZADAN OLISH VA TAYYORLASH ---
def load_and_prep_data():
    products = pd.read_sql("SELECT * FROM products", engine)
    sales = pd.read_sql("SELECT * FROM sales", engine)
    
    products.rename(columns={'cost_prise': 'cost_price'}, inplace=True)
    sales.rename(columns={'regiaon': 'region', 'pyment_type': 'payment_type'}, inplace=True)
    
    products.dropna(inplace=True)
    sales.dropna(inplace=True)
    sales = sales[(sales['price'] > 0) & (sales['quantity'] > 0)]
    products = products[products['cost_price'] > 0]
    
    sales['order_date'] = pd.to_datetime(sales['order_date'], errors='coerce')
    sales.dropna(subset=['order_date'], inplace=True)
    
    df = sales.merge(products[['product_id', 'cost_price', 'product_name']], on='product_id', how='left')
    df.dropna(subset=['cost_price'], inplace=True)
    df['revenue'] = df['price'] * df['quantity']
    df['profit'] = df['revenue'] - (df['cost_price'] * df['quantity'])
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    
    return df

df = load_and_prep_data()

# Dastlabki noutbukdagi kabi oylik guruhlangan ma'lumotlarni tayyorlab olamiz
def get_monthly_data():
    monthly = df.groupby('month').agg(
        revenue=('revenue', 'sum'),
        quantity=('quantity', 'sum'),
        profit=('profit', 'sum')
    ).reset_index()
    monthly = monthly.sort_values('month').reset_index(drop=True)
    return monthly


# --- API ENDPOINTLAR ---

@app.get("/")
def read_root():
    return {"message": "Business Analytics API tizimiga xush kelibsiz!"}

@app.get("/metrics")
def get_metrics():
    total_revenue = float(df['revenue'].sum())
    total_profit = float(df['profit'].sum())
    profit_margin = float((total_profit / total_revenue) * 100)
    
    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "profit_margin_percent": round(profit_margin, 2)
    }

@app.get("/top-products")
def get_top_products(limit: int = 10, sort_by: Literal["revenue", "quantity"] = "revenue"):
    """Tushum (revenue) yoki miqdor (quantity) bo'yicha eng yaxshi mahsulotlar ro'yxati"""
    
    # 1. Mahsulotlarni ham tushum, ham miqdor bo'yicha guruhlash va yig'indisini olish
    grouped_products = df.groupby('product_name').agg(
        revenue=('revenue', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()
    
    # 2. Foydalanuvchi tanlagan parametr (sort_by) bo'yicha kamayish tartibida saralash
    top_products = grouped_products.sort_values(by=sort_by, ascending=False).head(limit)
    
    # 3. JSON formatiga o'tkazish
    result = top_products.to_dict(orient='records')
    
    return {
        "sorted_by": sort_by,
        "limit": limit,
        "top_products": result
    }


@app.get("/sales-trend")
def get_sales_trend():
    """Oylik tushum va sotilgan mahsulotlar miqdori trendi"""
    
    # Oylar bo'yicha ham tushum, ham miqdorni guruhlab hisoblash
    trend = df.groupby('month').agg(
        revenue=('revenue', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()
    
    # Natijani JSON formatiga o'tkazish
    result = trend.to_dict(orient='records')
    
    return {"sales_trend": result}


@app.get("/region-performance")
def get_region_performance():
    """Hududlar bo'yicha tushum va sotilgan mahsulotlar miqdori"""
    
    # Hududlar bo'yicha ham tushum, ham miqdorni guruhlab hisoblash
    regions = df.groupby('region').agg(
        revenue=('revenue', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()
    
    # Tushum (revenue) bo'yicha eng yuqorisidan pastiga qarab saralash
    regions = regions.sort_values(by='revenue', ascending=False)
    
    # Natijani JSON formatiga o'tkazish
    result = regions.to_dict(orient='records')
    
    return {"region_performance": result}


# --- FORECASTING (BASHORATLASH) APILARI ---

@app.get("/forecast/linear-regression")
def get_forecast_lr():
    """Scikit-Learn Linear Regression yordamida keyingi oy bashorati"""
    monthly = get_monthly_data()
    
    # X - bu oylar indeksi (1, 2, 3...), y - bu bashorat qilinadigan qiymat
    X = np.array(monthly.index + 1).reshape(-1, 1)
    next_month_num = np.array([[len(monthly) + 1]]) # Kelgusi oy indeksi
    
    # Revenue uchun model
    model_rev = LinearRegression()
    model_rev.fit(X, monthly['revenue'].values)
    pred_rev = model_rev.predict(next_month_num)[0]
    
    # Quantity uchun model
    model_qty = LinearRegression()
    model_qty.fit(X, monthly['quantity'].values)
    pred_qty = model_qty.predict(next_month_num)[0]
    
    # Profit uchun model
    model_prof = LinearRegression()
    model_prof.fit(X, monthly['profit'].values)
    pred_prof = model_prof.predict(next_month_num)[0]
    
    return {
        "forecast_month": "2026-01",
        "predicted_revenue": round(float(pred_rev), 2),
        "predicted_quantity": round(float(pred_qty), 2),
        "predicted_profit": round(float(pred_prof), 2),
        "model_used": "Linear Regression (Machine Learning)"
    }

@app.get("/forecast/moving-average")
def get_forecast_ma(window: int = 3):
    """Moving Average (O'rtacha siljuvchi) yordamida keyingi oy bashorati"""
    monthly = get_monthly_data()
    
    # Oxirgi 'window' (qoida bo'yicha 3) oylik ma'lumotlarning o'rtachasi
    pred_rev = np.mean(monthly['revenue'].values[-window:])
    pred_qty = np.mean(monthly['quantity'].values[-window:])
    pred_prof = np.mean(monthly['profit'].values[-window:])
    
    return {
        "forecast_month": "2026-01",
        "predicted_revenue": round(float(pred_rev), 2),
        "predicted_quantity": round(float(pred_qty), 2),
        "predicted_profit": round(float(pred_prof), 2),
        "model_used": f"{window}-Month Moving Average"
    }