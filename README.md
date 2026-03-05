# 📊 E-Commerce Business Analysis & Sales Forecasting API Pipeline

Ushbu loyiha chakana savdo (elektron tijorat) ma'lumotlarini tozalash, biznes metrikalarini tahlil qilish, kelajakdagi savdo hajmini mashinali o'qitish (Machine Learning) yordamida prognoz qilish (Forecasting) va olingan natijalarni **REST API** orqali taqdim etish uchun qurilgan to'liq ma'lumotlar quvuri (Data Pipeline) hisoblanadi. Loyiha to'liq **Docker** muhitiga o'tkazilgan.

## 📂 Ma'lumotlar bazasi (Datasets)

Loyiha uchun ikkita asosiy ma'lumotlar jadvalidan foydalanildi:

**1. `products.csv` (Mahsulotlar katalogi):**
* `product_id`: Mahsulotning unikal raqami.
* `product_name`: Mahsulot nomi.
* `category`: Mahsulot tegishli bo'lgan toifa (masalan, Electronics, Furniture).
* `cost_price`: Mahsulotning ishlab chiqarish yoki kelish tannarxi.

**2. `sales.csv` (Sotuv tranzaksiyalari - 120,000 ta qator):**
* `order_id`: Buyurtmaning unikal raqami.
* `customer_id`: Mijozning raqami.
* `product_id`: Sotib olingan mahsulot raqami.
* `category`: Mahsulot toifasi.
* `price`: Sotuv narxi.
* `quantity`: Sotib olingan miqdor.
* `order_date`: Xarid amalga oshirilgan sana va vaqt.
* `region`: Mijoz hududi (viloyati).
* `payment_type`: To'lov usuli (Naqd, Karta va h.k).

---

## ⚙️ Loyiha bosqichlari (What we did)

Loyiha mantiqiy jihatdan 4 ta asosiy bosqichga bo'lingan:

### Bosqich 1: Data Cleaning & Preprocessing (Ma'lumotlarni tozalash)
Xom ma'lumotlarni tahlilga yaroqli holatga keltirish:
* Ustun nomlari standartlashtirildi.
* Bo'sh (Null) va takroriy (Duplicate) qiymatlar bazadan olib tashlandi.
* Mantiqqa to'g'ri kelmaydigan qatorlar (narx va miqdor <= 0 bo'lgan yozuvlar) tozalandi.
* Jadvallar `product_id` orqali birlashtirildi (Merge) va har bir tranzaksiya uchun **Tushum (Revenue)** hamda **Sof Foyda (Profit)** hisoblab chiqildi.

### Bosqich 2: Data Analytics & Business Intelligence (Biznes Tahlil)
Tozalangan ma'lumotlar asosida biznesning asosiy KPI metrikalari hisoblandi:
* **Umumiy metrikalar:** Tushum, xarajat va foyda qismlari hisoblanib, biznesning "Foyda marjasi" (Profit margin) aniqlandi.
* **Hududiy va Toifaviy baholash:** Qaysi viloyatlarda savdo eng past ekanligi, shuningdek, tushum bo'yicha eng kuchli "Top 10" mahsulotlar aniqlandi.

### Bosqich 3: Sales Forecasting (Savdolarni prognozlash)
Kelgusi (2026-yil Yanvar) oyi uchun kutilayotgan natijalarni bashorat qilish maqsadida 2 xil usul qo'llanildi:
* **Linear Regression (Chiziqli regressiya):** Scikit-Learn yordamida ML modeli o'qitildi.
* **Moving Average (O'rtacha siljuvchi):** Oxirgi oylik ma'lumotlarga tayangan holda ishlash uchun sozlangan dinamik model (yuqori aniqlik).

### Bosqich 4: Backend API & Dockerization (Tizimni integratsiya qilish)
Barcha tahliliy ma'lumotlarni tashqi dasturlarga (Frontend, Mobile App) uzatish uchun **FastAPI** yordamida RESTful API qurildi. Ma'lumotlar bevosita **PostgreSQL** bazasidan o'qib olinadigan qilib sozlandi. Butun tizim **Docker** va **Docker Compose** orqali izolyatsiya qilingan muhitda yig'ildi.

---

## 🔌 API Endpoints (Mavjud API'lar)

API server ishga tushgandan so'ng quyidagi endpoint'lardan foydalanish mumkin:

* `GET /metrics` - Asosiy biznes metrikalari (Jami tushum, foyda va foyda marjasi).
* `GET /top-products?limit=10&sort_by=revenue` - Eng yaxshi mahsulotlar ro'yxati (Tushum yoki Miqdor bo'yicha dinamik filtrlash).
* `GET /sales-trend` - Har bir oy uchun tushum va sotilgan miqdorlar xronologiyasi.
* `GET /region-performance` - Viloyatlar kesimida savdo unumdorligi.
* `GET /forecast/linear-regression` - Machine Learning (Chiziqli regressiya) yordamida kelgusi oy bashorati.
* `GET /forecast/moving-average?window=3` - O'rtacha siljuvchi usuli yordamida bashorat (necha oyga asoslanishini `window` parametri orqali boshqarish mumkin).

---

## 📈 Asosiy Natijalar va Xulosalar (Key Insights)

1. **Moliyaviy Sog'lomlik:** Biznesning sof foyda marjasi **31.08%** ni tashkil etadi. Bu juda yuqori va sog'lom operatsion boshqaruvdan dalolat beradi. (Umumiy tushum: ~$63.3M, Sof foyda: ~$19.6M).
2. **Katalizatorlar:** **"Electronics"** toifasi biznes uchun eng asosiy foyda keltiruvchi yo'nalish.
3. **Mintaqaviy rivojlanish:** **Andijon** hududi tushum bo'yicha eng oxirgi o'rinda. Bu hududda lokal reklama va dilerlik tarmoqlarini kuchaytirish tavsiya etiladi.
4. **Prognoz:** Moving Average modeliga ko'ra, keyingi oyda kutilayotgan umumiy tushum **~$2.6 mln**, sotiladigan mahsulotlar miqdori esa **~15,000 dona** bo'lishi bashorat qilindi.

---

## 🚀 Qanday ishga tushirish kerak? (How to run)

Loyiha to'liq Docker muhitida ishlashga tayyorlangan. Hech qanday qo'shimcha baza yoki kutubxonalarni qo'lda o'rnatish shart emas.

**1. Repozitoriyani kompyuterga yuklab oling (Clone):**
```bash
git clone [https://github.com/Jav0x1r01/BusinessAnalysis.git](https://github.com/Jav0x1r01/BusinessAnalysis.git)
cd BusinessAnalysis
```

**2. Docker orqali ishga tushiring:**
```bash
docker-compose up --build
```

**Nima sodir bo'ladi?**
* Avval `PostgreSQL` ma'lumotlar bazasi ko'tariladi.
* Avtomatik ravishda `load_to_db.py` skripti ishga tushib, CSV fayllardagi ma'lumotlarni bazaga yuklaydi.
* So'ngra `FastAPI` serveri ishga tushadi.

**3. API ni tekshirish:**
Brauzeringizda quyidagi manzilga kiring:
👉 **http://localhost:8000/docs**
*(Swagger UI orqali barcha API so'rovlarni to'g'ridan-to'g'ri brauzerda tekshirib ko'rishingiz mumkin).*

---

## 💻 Texnologiyalar (Tech Stack)
* **Backend:** FastAPI, Uvicorn, Python 3.11
* **Database & ORM:** PostgreSQL, SQLAlchemy, psycopg2-binary
* **Data Engineering & ML:** Pandas, NumPy, Scikit-Learn
* **DevOps:** Docker, Docker Compose, Bash Scripting
* **Data Analysis:** Jupyter Notebook, Matplotlib, Seaborn