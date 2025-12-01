📰 Google News Scraper (Streamlit Version)

Aplikasi web sederhana namun *powerful* untuk melakukan **scraping data berita** dari Google News secara otomatis. Dibangun menggunakan **Python** dan **Streamlit**, alat ini memungkinkan pengguna untuk mencari berita berdasarkan kata kunci, memfilter tanggal, dan mengunduh hasilnya dalam format **Excel (.xlsx)**.

Proyek ini menggunakan metode **RSS Feed Parsing** (tanpa Selenium/Browser), menjadikannya sangat ringan, cepat, dan stabil untuk dijalankan di server gratisan seperti Streamlit Cloud.

🔗 **Live Demo:** [Klik disini untuk mencoba aplikasi](https://news-scraper-faiq.streamlit.app)

---

## ✨ Fitur Utama

* 🚀 **Ultra Ringan & Cepat:** Menggunakan teknik HTTP Request & RSS Parsing, tidak memerlukan instalasi Google Chrome atau driver browser yang berat.
* 🔍 **Pencarian Fleksibel:** Cari berita berdasarkan kata kunci (Keyword) apa saja.
* 📅 **Filter Tanggal:** Bisa membatasi pencarian berita pada rentang tanggal tertentu (Start Date - End Date).
* 🔢 **Limit Data:** Atur jumlah maksimal berita yang ingin diambil.
* 🧹 **Auto ETL (Extract, Transform, Load):**
    * Membersihkan format tanggal menjadi lebih mudah dibaca.
    * Mengekstrak *keyword* penting dari judul berita secara otomatis.
* 💾 **Export ke Excel:** Unduh hasil scraping langsung menjadi file `.xlsx` yang rapi.
* 🔒 **Safe Mode:** Fitur pengaman agar riwayat pencarian tidak hilang jika tab tidak sengaja tertutup.

---

## 🛠️ Teknologi yang Digunakan

* **[Python](https://www.python.org/)** - Bahasa pemrograman utama.
* **[Streamlit](https://streamlit.io/)** - Framework untuk membuat antarmuka web (Frontend).
* **[Pandas](https://pandas.pydata.org/)** - Untuk manipulasi data dan pembuatan tabel.
* **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** - Untuk parsing data XML/HTML dari Google News.
* **[Requests](https://pypi.org/project/requests/)** - Untuk mengirim permintaan HTTP ke server Google.
