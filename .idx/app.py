import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import time

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="News Scraper Lite", page_icon="⚡", layout="centered")

st.title("⚡ Google News Scraper (Lite)")
st.caption("Versi Ultra Ringan tanpa Browser. Cepat & Anti-Crash.")

# --- 2. FUNGSI SCRAPING (METODE RSS) ---
def scrape_rss(keyword, limit=50):
    # Menggunakan Jalur RSS Feed Google News (Legal & Ringan)
    base_url = "https://news.google.com/rss/search"
    
    # Parameter untuk Bahasa Indonesia
    params = {
        "q": keyword,
        "hl": "id-ID",
        "gl": "ID",
        "ceid": "ID:id"
    }
    
    # Fake User Agent agar diterima Google
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Request langsung tanpa buka browser
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status() # Cek error koneksi
        
        # Parsing data XML
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all("item")
        
        data = []
        
        # Loop data berita
        for index, item in enumerate(items):
            if index >= limit: break # Batasi jumlah
            
            title = item.title.text if item.title else "Tanpa Judul"
            link = item.link.text if item.link else "#"
            pub_date = item.pubDate.text if item.pubDate else "-"
            source = item.source.text if item.source else "Google News"
            
            data.append({
                "Judul": title,
                "Sumber": source,
                "Waktu Publish": pub_date,
                "Link": link
            })
            
        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return pd.DataFrame()

# --- 3. UI ---
with st.form("search_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        keyword = st.text_input("Kata Kunci", "IKN Nusantara")
    with col2:
        limit = st.number_input("Maksimal Data", 10, 100, 20)
    
    submitted = st.form_submit_button("Mulai Scraping 🚀")

if submitted:
    with st.spinner("Sedang mengambil data dari Google..."):
        # Simulasi loading biar kerasa ada prosesnya
        time.sleep(1)
        df = scrape_rss(keyword, limit)
    
    if not df.empty:
        st.success(f"Berhasil mendapatkan {len(df)} berita!")
        st.dataframe(df, use_container_width=True)
        
        # Download Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            
        st.download_button(
            label="📥 Download Excel",
            data=output.getvalue(),
            file_name=f"news_{keyword}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Tidak ditemukan berita atau terjadi kesalahan koneksi.")