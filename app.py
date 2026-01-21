import streamlit as st
import json
import random
import time
import streamlit.components.v1 as components

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Latihan Keamanan Siber",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. DUMMY DATA (Tambahkan field 'explanation' jika perlu) ---
DEFAULT_QUESTIONS = [
    {
        "id": 1,
        "type": "single",
        "question": "Apa itu SQL Injection?",
        "options": {"A": "Enkripsi database", "B": "Token authentication", "C": "Menjalankan SQL berbahaya pada database", "D": "Manipulasi HTTP Header"},
        "correct": ["C"],
        "explanation": "SQL Injection terjadi ketika input pengguna yang tidak divalidasi disisipkan ke dalam query SQL, memungkinkan penyerang memanipulasi database."
    },
    {
        "id": 2,
        "type": "single",
        "question": "Kapan UU PDP No. 27 Tahun 2022 disahkan?",
        "options": {"A": "17 Oktober 2022", "B": "17 Agustus 2022", "C": "27 September 2022", "D": "1 Januari 2023"},
        "correct": ["A"],
        "explanation": "UU Pelindungan Data Pribadi (PDP) disahkan oleh DPR pada tanggal 17 Oktober 2022."
    },
    {
        "id": 3,
        "type": "multiple",
        "question": "Manakah yang termasuk jenis serangan siber? (Pilih 2)",
        "options": {"A": "Phishing", "B": "Debugging", "C": "DDoS", "D": "Coding"},
        "correct": ["A", "C"],
        "explanation": "Phishing (penipuan) dan DDoS (membanjiri trafik) adalah serangan. Debugging dan Coding adalah aktivitas pemrograman."
    }
]

# --- 3. LOAD DATA ---
@st.cache_data
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_QUESTIONS

questions = load_questions()

# --- 4. CSS (Fix Warna Teks) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp { background-color: #f8f9fa; font-family: 'Inter', sans-serif; }
    .block-container { max-width: 800px; padding-top: 2rem; }

    /* Card Styling */
    .question-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 10px;
        border: 1px solid #e9ecef;
    }
    
    .question-text {
        font-size: 1.15rem; 
        font-weight: 600; 
        color: #2d3748; 
        margin-bottom: 0.5rem;
    }

    .question-badge {
        background-color: #e2e8f0; color: #4a5568;
        padding: 4px 12px; border-radius: 20px;
        font-size: 0.85rem; font-weight: 600;
        display: inline-block; margin-bottom: 10px;
    }

    /* FIX WARNA TEKS */
    .stRadio label p, .stCheckbox label p { color: #1a202c !important; font-size: 1rem; }
    div[role="radiogroup"], div[data-baseweb="checkbox"] {
        background-color: white; padding: 10px; border-radius: 8px; border: 1px solid #edf2f7;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        font-size: 0.9rem;
        color: #3182ce;
        font-weight: 600;
    }

    /* Hide Elements */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 5. SESSION STATE ---
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
    st.session_state.quiz_data = random.sample(questions, len(questions))
    for q in st.session_state.quiz_data:
        items = list(q["options"].items())
        random.shuffle(items)
        q["shuffled_options"] = items

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# --- 6. UI UTAMA ---
st.markdown("<h1>🛡️ Latihan Keamanan Siber</h1>", unsafe_allow_html=True)

# --- 7. FORM SOAL ---
if not st.session_state.submitted:
    with st.form(key='quiz_form'):
        for i, q in enumerate(st.session_state.quiz_data):
            
            # 1. Kartu Soal
            st.markdown(f"""
            <div class="question-card">
                <span class="question-badge">Soal {i + 1}</span>
                <div class="question-text">{q['question']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 2. Pilihan Jawaban
            labels = [f"{k}. {v}" for k, v in q["shuffled_options"]]
            
            if q["type"] == "single":
                st.radio("Pilih:", labels, key=f"ans_{q['id']}", index=None, label_visibility="collapsed")
            else:
                for label in labels:
                    st.checkbox(label, key=f"ans_{q['id']}_{label}")
            
            # --- FITUR BARU: INTIP JAWABAN ---
            # Kita gunakan st.expander agar tidak men-trigger submit form
            with st.expander(f"💡 Bingung? Lihat Kunci Jawaban Soal {i+1}"):
                # Ambil teks jawaban yang benar
                correct_list = []
                for k in q['correct']:
                    # Ambil teks asli dari opsi (misal: "A" -> "Enkripsi database")
                    val = q['options'].get(k, "Tidak ditemukan")
                    correct_list.append(f"**({k}) {val}**")
                
                # Tampilkan
                st.info(f"Jawaban Benar: {', '.join(correct_list)}")
                
                # Tampilkan penjelasan jika ada di JSON
                if "explanation" in q:
                    st.markdown(f"**Penjelasan:** {q['explanation']}")
            
            st.markdown("<br>", unsafe_allow_html=True)

        submit_btn = st.form_submit_button("🔒 SELESAI & CEK SKOR")
        if submit_btn:
            st.session_state.submitted = True
            st.rerun()

else:
    # --- HASIL AKHIR ---
    score = 0
    total = len(st.session_state.quiz_data)
    
    for q in st.session_state.quiz_data:
        correct_keys = q["correct"]
        if q["type"] == "single":
            ans_key = f"ans_{q['id']}"
            if ans_key in st.session_state and st.session_state[ans_key]:
                if st.session_state[ans_key].split(".")[0] in correct_keys:
                    score += 1
        else:
            # Hitung checkbox
            selected = []
            for k, v in q["shuffled_options"]:
                if st.session_state.get(f"ans_{q['id']}_{k}. {v}", False):
                    selected.append(k)
            if set(selected) == set(correct_keys):
                score += 1

    final_score = (score / total) * 100
    
    st.balloons()
    st.markdown(f"""
    <div style="text-align:center; padding: 2rem; background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h2 style="color: #2d3748;">Latihan Selesai!</h2>
        <div style="font-size: 3rem; font-weight: bold; color: #3182ce;">{final_score:.0f}</div>
        <p>Skor Anda</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Ulangi Latihan"):
        st.session_state.clear()
        st.rerun()
