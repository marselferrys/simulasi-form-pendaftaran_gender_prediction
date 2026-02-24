import streamlit as st
from gradio_client import Client

# Konfigurasi halaman (Wajib diletakkan paling atas)
st.set_page_config(page_title="Form Pendaftaran", page_icon="🎓")

# 1. Inisialisasi Client (Gunakan cache agar tidak reload/koneksi ulang terus menerus)
@st.cache_resource
def get_hf_client():
    API_URL = "marselferrys/indo_name-gender-prediction"
    return Client(API_URL)

client = get_hf_client()

# 2. Fungsi Callback untuk Auto-fill
def autofill_gender():
    # Mengambil nilai nama dari session_state (apa yang sedang diketik user)
    nama = st.session_state.nama_input
    
    if not nama or len(nama.strip()) < 3:
        return

    try:
        # Menembak API Hugging Face (Gunakan fn_index=0 untuk menghindari error)
        result = client.predict(
                nama, # Mengirim langsung isi dari in_nama
                api_name="/predict"
        )
        
        # Ambil hasil dan bersihkan
        gender_api_result = str(result[0]).strip().upper()

        # Update Radio Button secara otomatis melalui session_state
        if gender_api_result == "M":
            st.session_state.gender_input = "Laki-laki"
        elif gender_api_result == "F":
            st.session_state.gender_input = "Perempuan"

    except Exception as e:
        # Jika API gagal, kita biarkan saja (user bisa milih manual)
        pass 


# ==========================================
# ANTARMUKA FORMULIR PENDAFTARAN (UI)
# ==========================================

st.title("🎓 Form Pendaftaran Mahasiswa Baru")
st.markdown("Silakan lengkapi data diri di bawah ini dengan benar.")

# Input Nama -> Parameter on_change akan memicu fungsi autofill_gender saat user menekan Enter/keluar dari kolom
st.text_input(
    "Nama Lengkap", 
    placeholder="Jangan disingkat, Contoh: Budi Santoso Kesuma", 
    key="nama_input", 
    on_change=autofill_gender
)

st.text_input("NIM", placeholder="121140xxx", key="nim_input")

st.selectbox(
    "Program Studi", 
    ["Pilih Program Studi",
  "Teknik Informatika",
  "Sains Data",
  "Fisika",
  "Matematika",
  "Biologi",
  "Kimia",
  "Farmasi",
  "Sains Atmosfer dan Keplanetan",
  "Sains Aktuaria",
  "Sains Lingkungan Kelautan",
  "Teknik Geomatika",
  "Perencanaan Wilayah dan Kota",
  "Teknik Sipil",
  "Arsitektur",
  "Teknik Lingkungan",
  "Teknik Kelautan",
  "Desain Komunikasi Visual",
  "Arsitektur Lanskap",
  "Teknik Perkeretaapian",
  "Rekayasa Tata Kelola Air Terpadu",
  "Pariwisata",
  "Teknik Elektro",
  "Teknik Geofisika",
  "Teknik Geologi",
  "Teknik Mesin",
  "Teknik Industri",
  "Teknik Kimia",
  "Teknik Fisika",
  "Teknik Biosistem",
  "Teknologi Industri Pertanian",
  "Teknologi Pangan",
  "Teknik Sistem Energi",
  "Teknik Pertambangan",
  "Teknik Material",
  "Teknik Telekomunikasi",
  "Rekayasa Kehutanan",
  "Teknik Biomedik",
  "Rekayasa Kosmetik",
  "Rekayasa Minyak dan Gas",
  "Rekayasa Instrumentasi dan Automasi"
], 
    key="prodi_input"
)

# Radio Button Jenis Kelamin (Index=None agar awalnya kosong sebelum sistem menebak)
st.radio(
    "Jenis Kelamin", 
    ["Laki-laki", "Perempuan"], 
    index=None, 
    key="gender_input"
)

st.markdown("---") # Garis pemisah

# Tombol Submit
if st.button("💾 Submit Pendaftaran", type="primary", use_container_width=True):
    # Ambil semua data saat tombol diklik
    nama = st.session_state.nama_input
    nim = st.session_state.nim_input
    prodi = st.session_state.prodi_input
    gender = st.session_state.gender_input

    # Validasi
    if not nama or not nim or not gender or not prodi:
        st.error("❌ Gagal: Pastikan Nama, NIM, Prodi, dan Jenis Kelamin telah terisi!")
    else:
        # Tampilan pesan sukses yang rapi
        st.success(f"""
        ✅ **Pendaftaran Berhasil Disimpan!**
        
        **Rincian Data Mahasiswa:**
        * **Nama Lengkap** : {nama}
        * **NIM** : {nim}
        * **Program Studi**: {prodi}
        * **Jenis Kelamin**: {gender}
        """)
