# Applicant Tracking System (ATS)

Sistem ini merupakan implementasi **Applicant Tracking System (ATS)** berbasis pencocokan kata kunci pada file CV digital. Sistem memungkinkan pencarian kandidat berdasarkan *keyword* yang dimasukkan oleh pengguna, menggunakan algoritma pencocokan string klasik dan modern, serta mendukung ekstraksi informasi dan enkripsi data kandidat.

---

## 🔍 Algoritma Pencocokan Pola

### 1. Knuth-Morris-Pratt (KMP)

KMP adalah algoritma pencocokan string yang efisien untuk menemukan pola dalam teks. KMP menghindari pencocokan karakter yang sudah dibandingkan sebelumnya dengan membangun tabel **Longest Prefix Suffix (LPS)**, yang memungkinkan algoritma untuk "melompat" ke posisi yang tepat saat terjadi *mismatch*.

- **Kompleksitas Waktu:** `O(n + m)`  
  `n = panjang teks`, `m = panjang pola`
- Cocok untuk: pencarian cepat satu keyword dalam satu CV

---

### 2. Boyer-Moore (BM)

Boyer-Moore adalah algoritma pencocokan pola yang bekerja dari **kanan ke kiri** dan memanfaatkan dua heuristik:  
- **Bad Character Rule**
- **Good Suffix Rule**

BM sangat efisien terutama pada teks panjang karena mampu melewati karakter-karakter tidak relevan secara cepat.

- **Kompleksitas Rata-rata:** Sublinear  
- Cocok untuk: pencarian satu keyword pada dokumen besar

---

### 3. (Bonus) Aho-Corasick

Aho-Corasick digunakan untuk mencocokkan **banyak keyword sekaligus** hanya dalam **satu lintasan teks**. Algoritma ini membangun struktur automaton berbasis **Trie** dengan **fail function**, mirip finite automata.

- **Kompleksitas Waktu:** `O(n + total length keyword)`  
- Cocok untuk: multi-keyword search pada CV dalam jumlah besar

---


# Requirements dan Cara Menjalankan Program

This project uses [`uv`](https://github.com/astral-sh/uv), a fast alternative to `pip` and `virtualenv`.

## Requirements

* Python 3.8 or higher
* `uv` installed on your system. If not, install it using:

```bash
pip install uv
```
## Docker

### 1. Open root directory in terminal
```bash
cd path
```

### 2. Run MySQL container with docker
```bash
docker compose up -d
```


## How to Run

### 1. Create and activate virtual environment with `uv`

```bash
uv venv
source .venv/bin/activate  # For bash (Linux/macOS)

# For Windows PowerShell
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 3. Run the application

```bash
uv run src/main.py
```

# Author
1. Dita Maheswari 13523125
2. Ahmad Syafiq 13523135
3. Juan Sohuturon Arauna Siagian 18222086
