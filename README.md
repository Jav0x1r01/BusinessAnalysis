# 📊 E-Commerce Business Analysis & Sales Forecasting Pipeline

Ushbu loyiha chakana savdo (elektron tijorat) ma'lumotlarini tozalash, biznes metrikalarini tahlil qilish va kelajakdagi savdo hajmini mashinali o'qitish (Machine Learning) hamda statistik modellar yordamida prognoz qilish (Forecasting) uchun qurilgan to'liq ma'lumotlar quvuri (Data Pipeline) hisoblanadi.

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

Loyiha mantiqiy jihatdan 3 ta asosiy bosqichga bo'lingan:

### Bosqich 1: Data Cleaning & Preprocessing (Ma'lumotlarni tozalash)
Xom ma'lumotlarni tahlilga yaroqli holatga keltirish uchun quyidagi ishlar amalga oshirildi:
* Ustun nomlari standartlashtirildi (`cost_prise` -> `cost_price`, `regiaon` -> `region`).
* Bo'sh (Missing/Null) va takroriy (Duplicate) qiymatlar bazadan olib tashlandi.
* Mantiqqa to'g'ri kelmaydigan qatorlar (narx va miqdor <= 0 bo'lgan yozuvlar) tozalandi.
* Matn formatidagi sanalar (`order_date`) to'g'ri `datetime` formatiga o'girildi va xato sanalar o'chirildi.
* Ikki jadval `product_id` orqali birlashtirildi (Merge) va har bir tranzaksiya uchun **Tushum (Revenue)** hamda **Sof Foyda (Profit)** hisoblab chiqildi.

### Bosqich 2: Data Analytics & Business Intelligence (Biznes Tahlil)
Tozalangan ma'lumotlar asosida biznesning asosiy KPI metrikalari va vizualizatsiyalar vizual tahlil qilindi:
* **Umumiy metrikalar:** Tushum, xarajat va foyda qismlari hisoblanib, biznesning "Foyda marjasi" (Profit margin) aniqlandi.
* **Kategoriyalar va Mahsulotlar:** Tushum bo'yicha "Top 10" eng zo'r mahsulotlar hamda eng ko'p foyda keltiruvchi toifalar gorizontal grafiklarda tasvirlandi.
* **Hududiy baholash:** Qaysi viloyatlarda savdo eng past ekanligi aniqlanib, e'tibor qaratilishi kerak bo'lgan bo'shliqlar topildi.
* **Trend va Xatti-harakatlar:** Oylik savdo o'sish dinamikasi chiziqli grafikda (line chart), tranzaksiyalarning ish va dam olish kunlariga, shuningdek, to'lov turlariga qarab taqsimoti doiraviy (pie chart) grafiklarda ochib berildi.

### Bosqich 3: Sales Forecasting (Savdolarni prognozlash)
Kelgusi (2026-yil Yanvar) oyi uchun kutilayotgan natijalarni bashorat qilish maqsadida ma'lumotlar oylik formatga o'tkazildi va 2 xil usul qo'llanildi:
* **Linear Regression (Chiziqli regressiya):** Trendni aniqlash maqsadida qo'llanildi, biroq biznes mavsumiylikka ega bo'lgani uchun aniqlik ko'rsatkichi (R-squared) past chiqdi.
* **Moving Average (O'rtacha siljuvchi):** Oxirgi 3 oylik ma'lumotlarga tayangan holda ishlash uchun sozlangan bu model o'zini oqladi va **~2.6% xatolik (MAPE)** bilan yuqori aniqlikdagi prognozlarni taqdim etdi.

---

## 📈 Asosiy Natijalar va Xulosalar (Key Insights)

1. **Moliyaviy Sog'lomlik:** Biznesning sof foyda marjasi **31.08%** ni tashkil etadi. Bu juda yuqori va sog'lom operatsion boshqaruvdan dalolat beradi. (Umumiy tushum: ~$63.3M, Sof foyda: ~$19.6M).
2. **Katalizatorlar:** **"Electronics"** toifasi biznes uchun eng asosiy foyda keltiruvchi yo'nalish hisoblanadi. Asosiy e'tibor va zaxiralar shu yo'nalishga qaratilishi kerak.
3. **Mintaqaviy rivojlanish:** **Andijon** hududi tushum bo'yicha eng oxirgi o'rinda. Bu hududda yetkazib berish, lokal reklama va dilerlik tarmoqlarini kuchaytirish tavsiya etiladi.
4. **Prognoz:** O'rtacha siljuvchi (Moving Average) modeliga ko'ra, keyingi oyda kutilayotgan umumiy tushum **~$2.6 mln**, sotiladigan mahsulotlar miqdori esa **~15,000 dona** ekanligi bashorat qilindi. Omborda ayniqsa Electronics va Furniture toifalari zaxiralarini tayyorlash talab etiladi.

---

## 🚀 Qanday ishga tushirish kerak? (How to run)

Loyihani o'z kompyuteringizda ishga tushirish uchun quyidagi qadamlarni bajaring:

**1. Repozitoriyani yuklab oling (Clone):**
```bash
git clone [https://github.com/Jav0x1r01/BusinessAnalysis.git](https://github.com/Jav0x1r01/BusinessAnalysis.git)
cd BusinessAnalysis
```

**2. Kerakli kutubxonalarni o'rnating:**
Dastur to'g'ri ishlashi uchun quyidagi Python kutubxonalari o'rnatilgan bo'lishi kerak:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

**3. Jupyter Notebook'ni ishga tushiring:**
```bash
jupyter notebook
```
Brauzeringizda ochilgan oynadan `data_pipeline.ipynb` faylini tanlang va kodlarni yuqoridan pastga qarab ishga tushiring (`Shift + Enter`).

---

## 💻 Texnologiyalar (Tech Stack)
* **Dasturlash tili:** Python 3
* **Ma'lumotlar tahlili va tozalash:** Pandas, NumPy
* **Vizualizatsiya:** Matplotlib, Seaborn
* **Mashinali o'qitish (ML):** Scikit-Learn (Linear Regression)
* **Muhit:** Jupyter Notebook