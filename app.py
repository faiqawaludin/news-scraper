import streamlit as st
import streamlit.components.v1 as components # Library untuk menyuntikkan JavaScript
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="Scraper Pengumpul Data Berita", page_icon="🚀", layout="centered")

with st.sidebar:
    st.header("⚙️ Pengaturan")
    enable_lock = st.checkbox("🔒 Kunci Halaman (Cegah Close/Refresh)", value=True, help="Jika dicentang, browser akan bertanya konfirmasi sebelum tab ditutup agar riwayat tidak hilang.")

if enable_lock:
    js_warning = """
    <script>
        // Fungsi untuk memunculkan peringatan browser
        function onBeforeUnload(e) {
            e.preventDefault();
            e.returnValue = ''; // Wajib ada untuk Chrome/Edge
            return '';
        }
        
        // Pasang "Gembok" ke jendela browser utama
        window.parent.addEventListener('beforeunload', onBeforeUnload);
    </script>
    """
    components.html(js_warning, height=0)
else:
    js_release = """
    <script>
        // Hapus listener agar bisa keluar bebas
        // Catatan: Karena iframe streamlit agak unik, cara paling efektif melepasnya 
        // adalah dengan me-refresh komponen, tapi di sini kita biarkan kosong 
        // karena saat checkbox uncheck, komponen script di atas otomatis hilang.
        // Tapi untuk memastikan bersih di sisi parent:
        window.parent.removeEventListener('beforeunload', window.parent.onBeforeUnload);
    </script>
    """
    components.html(js_release, height=0)


st.title("🚀 Google News Scraper")
st.markdown("Tools untuk membantu mengumpulkan data berita.")

if 'history' not in st.session_state:
    st.session_state['history'] = []

def extract_keywords(title, search_keyword):
    stop_words = ["dan", "di", "dari", "yang", "dengan", "untuk", "dalam", "pada", "ini", "itu", "ke", "akan", search_keyword.lower()]
    words = title.lower().split()
    filtered = [w.strip(".,:;!?()'\"") for w in words if w not in stop_words and len(w) > 3]
    seen = set()
    final = []
    for w in filtered:
        if w not in seen:
            seen.add(w)
            final.append(w)
            if len(final) >= 5: break
    return ", ".join(final)

def format_date_rss(date_str):
    try:
        dt_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
        return dt_obj.strftime("%d %b %Y")
    except:
        return date_str

def scrape_rss(keyword, limit, start_date=None, end_date=None, use_date=False):
    base_url = "https://news.google.com/rss/search"
    search_query = keyword
    if use_date and start_date and end_date:
        str_start = start_date.strftime("%Y-%m-%d")
        str_end = end_date.strftime("%Y-%m-%d")
        search_query = f"{keyword} after:{str_start} before:{str_end}"
    
    params = {"q": search_query, "hl": "id-ID", "gl": "ID", "ceid": "ID:id"}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all("item")
        data = []
        for index, item in enumerate(items):
            if index >= limit: break
            
            raw_title = item.title.text if item.title else "Tanpa Judul"
            raw_link = item.link.text if item.link else "#"
            raw_date = item.pubDate.text if item.pubDate else "-"
            raw_source = item.source.text if item.source else "Google News"
            
            clean_date = format_date_rss(raw_date)
            keywords = extract_keywords(raw_title, keyword)
            
            data.append({
                "Judul": raw_title,
                "Sumber": raw_source,
                "Tanggal": clean_date,
                "Keywords": keywords,
                "Link": raw_link
            })
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return pd.DataFrame()

tab1, tab2 = st.tabs(["🔍 Tools Scraper", "📜 Riwayat Sesi"])

with tab1:
    with st.container(border=True):
        st.subheader("Parameter Pencarian")
        keyword_input = st.text_input("Masukkan Kata Kunci", placeholder="Contoh: Pilkada 2024")
        col1, col2 = st.columns(2)
        with col1:
            limit_input = st.number_input("Maksimal Data", 10, 100, 50)
        with col2:
            use_date = st.checkbox("Filter Rentang Tanggal")
        
        start_d, end_d = None, None
        if use_date:
            c_date1, c_date2 = st.columns(2)
            with c_date1:
                start_d = st.date_input("Dari Tanggal", value=datetime.today() - timedelta(days=7))
            with c_date2:
                end_d = st.date_input("Sampai Tanggal", value=datetime.today())

        st.write("")
        btn_start = st.button("Mulai Scraping 🚀", type="primary", use_container_width=True)

    if btn_start:
        if not keyword_input:
            st.warning("⚠️ Harap masukkan kata kunci.")
        else:
            st.divider()
            with st.spinner("Sedang mengambil data..."):
                time.sleep(0.5)
                df = scrape_rss(keyword_input, limit_input, start_d, end_d, use_date)
            
            if not df.empty:
                st.success(f"✅ Berhasil mendapatkan **{len(df)}** berita!")
                st.dataframe(df, use_container_width=True)
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                history_item = {
                    "time": timestamp,
                    "keyword": keyword_input,
                    "count": len(df),
                    "data": df
                }
                st.session_state['history'].insert(0, history_item)
                
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Hasil')
                
                file_name = f"News_{keyword_input.replace(' ', '_')}.xlsx"
                st.download_button("📥 Download Excel", output.getvalue(), file_name, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
            else:
                st.error("❌ Tidak ditemukan berita.")


with tab2:
    if enable_lock:
        st.success("🔒 **Mode Aman Aktif**: Browser akan mencegah tab tertutup tidak sengaja.")
    else:
        st.warning("🔓 **Mode Aman Mati**: Hati-hati, jika tab tertutup, riwayat di bawah ini akan hilang.")

    st.divider()
    
    if not st.session_state['history']:
        st.write("Belum ada riwayat pencarian.")
    else:
        for i, item in enumerate(st.session_state['history']):
            with st.expander(f"⏰ {item['time']} - Keyword: **{item['keyword']}** ({item['count']} Data)"):
                st.dataframe(item['data'], use_container_width=True)
                output_hist = BytesIO()
                with pd.ExcelWriter(output_hist, engine='xlsxwriter') as writer:
                    item['data'].to_excel(writer, index=False, sheet_name='Hasil')
                st.download_button(f"📥 Download Excel ({item['keyword']})", output_hist.getvalue(), f"History_{item['keyword']}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key=f"dl_{i}")

st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f0f2f6; /* Warna latar abu muda, sesuaikan jika dark mode */
            color: #333;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            z-index: 100;
            border-top: 1px solid #ddd;
        }
        @media (prefers-color-scheme: dark) {
            .footer {
                background-color: #0e1117;
                color: #fafafa;
                border-top: 1px solid #333;
            }
        }
    </style>
    <div class="footer">
        Made with ❤️ by <b>Faiq Awaludin</b>
    </div>
    """, unsafe_allow_html=True)