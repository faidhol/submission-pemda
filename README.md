# 🛍️ ETL Pipeline – Fashion Studio Data

Proyek ini merupakan implementasi **ETL (Extract, Transform, Load) Pipeline** untuk mengambil data produk dari website Fashion Studio, membersihkan data, dan menyimpannya ke beberapa tujuan penyimpanan.

Pipeline dibangun menggunakan prinsip **Modular Code Architecture** dengan pemisahan tahap Extract, Transform, dan Load dalam file terpisah.

---

## 📌 Project Overview

Pipeline ini melakukan:

1. **Extract**  
   Mengambil data produk dari website:
   https://fashion-studio.dicoding.dev/

2. **Transform**  
   Membersihkan dan memvalidasi data:
   - Konversi harga USD → IDR
   - Ekstraksi nilai numerik dari rating & colors
   - Menghapus data invalid
   - Menghapus duplikasi
   - Type enforcement

3. **Load**  
   Menyimpan data ke:
   - CSV File
   - Google Sheets
   - PostgreSQL Database

---

## 🏗️ Project Structure

```
project/
│
├── main.py
├── requirements.txt
├── products.csv
├── etl.log
├── .env
│
├── utils/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── logger.py
│
├── google-sheets-api.json
└── README.md
```

---

## ⚙️ Installation

1. Clone repository

```bash
git clone <repository-url>
cd <project-folder>
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Setup environment variable

Buat file `.env`:

```
DATABASE_URL=postgresql://user:password@host:port/dbname
```

4. Setup Google Sheets API

- Buat Service Account
- Download credential JSON
- Rename menjadi:

```
google-sheets-api.json
```

---

## 🚀 How to Run

```bash
python main.py
```

Jika berhasil, output:

```
ETL PIPELINE COMPLETED SUCCESSFULLY
```

---

## 🧪 Testing

Menjalankan unit test:

```bash
pytest
```

Coverage test:

```bash
pytest --cov
```

---

## 📊 Data Transformation Details

### Price
- Menghapus simbol `$`
- Menghapus koma
- Konversi ke numeric
- Dikonversi ke IDR (kurs tetap: 16.000)

### Rating
- Ekstraksi angka desimal
- Validasi maksimum 5

### Colors
- Ekstraksi jumlah warna (integer)

### Validation Rules
- Harga harus > 0
- Rating ≤ 5
- Title tidak boleh "Unknown Product"
- Drop duplicates

---

## 📝 Logging

Semua proses dicatat dalam:

```
etl.log
```

Logging mencatat:
- Jumlah data extract
- Jumlah data setelah transform
- Status load
- Error handling

---

## 🛠️ Technologies Used

- Python
- Requests
- BeautifulSoup
- Pandas
- SQLAlchemy
- PostgreSQL
- Google Sheets API
- Pytest

---

## 🎯 Key Features

- Modular ETL architecture
- Retry mechanism pada extract
- Data validation & cleaning
- Multi-destination loading
- Logging system
- Environment variable support
- Unit testing support

---

## 📌 Notes

- URL pagination mengikuti pola:
  - `/` untuk halaman pertama
  - `/page2`, `/page3`, dst
- Tidak menggunakan query parameter `?page=` untuk menghindari duplikasi data.

---

## ✅ Submission Checklist

- [x] Modular ETL (Extract, Transform, Load)
- [x] Logging implemented
- [x] Environment variable for DB
- [x] Google Sheets integration
- [x] PostgreSQL integration
- [x] Clean data validation
- [x] requirements.txt included
- [x] README documentation complete

---

## 👤 Author

Nama: [Isi Nama Anda]  
Project: ETL Fashion Studio Data  
Year: 2026

---