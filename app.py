import streamlit as st
import json
import random
import time
import streamlit.components.v1 as components

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CBT Keamanan Siber",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. DUMMY DATA ---
DEFAULT_QUESTIONS = [
    {
        "id": 1,
        "type": "single",
        "question": "Apa itu SQL Injection?",
        "options": {"A": "Enkripsi database", "B": "Token authentication", "C": "Menjalankan SQL berbahaya pada database", "D": "Manipulasi HTTP Header"},
        "correct": ["C"]
    },
    {
        "id": 2,
        "type": "single",
        "question": "Kapan UU PDP No. 27 Tahun 2022 disahkan?",
        "options": {"A": "17 Oktober 2022", "B": "17 Agustus 2022", "C": "27 September 2022", "D": "1 Januari 2023"},
        "correct": ["A"]
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

# --- 4. CSS DENGAN PERBAIKAN WARNA TEKS ---
st.markdown("""
<style>
    /* Font & Base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Inter', sans-serif;
    }
    
    /* Container Utama */
    .block-container {
        max-width: 800px;
        padding-top: 2rem;
    }

    /* Card Styling */
    .question-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 10px; /* Jarak antara soal dan opsi */
        border: 1px solid #e9ecef;
    }
    
    .question-text {
        font-size: 1.15rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }

    .question-badge {
        background-color: #e2e8f0;
        color: #4a5568;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* --- PERBAIKAN PENTING: WARNA TEKS OPSI --- */
    /* Memaksa teks radio button (pilihan ganda) berwarna hitam */
    .stRadio label p, .stCheckbox label p {
        color: #1a202c !important; /* Hitam pekat */
        font-size: 1rem;
    }
    
    /* Styling Container Opsi agar lebih rapi */
    div[role="radiogroup"], div[data-baseweb="checkbox"] {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #edf2f7;
    }

    /* Tombol Submit */
    .stButton > button {
        background-color: #3182ce;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        width: 100%;
        margin-top: 20px;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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

# --- 6. TIMER LOGIC ---
DURATION_SEC = 30 * 60 
elapsed = time.time() - st.session_state.start_time
remaining_sec = max(0, DURATION_SEC - elapsed)

if remaining_sec <= 0 and not st.session_state.submitted:
    st.session_state.submitted = True
    st.warning("Waktu Habis!")

# --- 7. UI UTAMA ---
st.markdown("<h1>🛡️ CBT Keamanan Siber</h1>", unsafe_allow_html=True)

# Timer HTML
if not st.session_state.submitted:
    timer_html = f"""
        <div style="text-align: center; color: #e53e3e; background: #fff5f5; padding: 10px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #fed7d7; font-weight: bold;">
            ⏱️ Sisa Waktu: <span id="timer">--:--</span>
        </div>
        <script>
        var timeLeft = {int(remaining_sec)};
        var timerElem = document.getElementById('timer');
        var countdown = setInterval(function() {{
            if(timeLeft <= 0) {{ clearInterval(countdown); timerElem.innerHTML = "WAKTU HABIS"; }} 
            else {{
                var m = Math.floor(timeLeft / 60);
                var s = timeLeft % 60;
                timerElem.innerHTML = m + "m " + (s < 10 ? "0" : "") + s + "s";
                timeLeft--;
            }}
        }}, 1000);
        </script>
    """
    components.html(timer_html, height=70)

# --- 8. FORM SOAL ---
if not st.session_state.submitted:
    with st.form(key='quiz_form'):
        for i, q in enumerate(st.session_state.quiz_data):
            # Tampilan Soal
            st.markdown(f"""
            <div class="question-card">
                <span class="question-badge">Soal {i + 1}</span>
                <div class="question-text">{q['question']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tampilan Opsi
            labels = [f"{k}. {v}" for k, v in q["shuffled_options"]]
            
            if q["type"] == "single":
                st.radio("Pilih:", labels, key=f"ans_{q['id']}", index=None, label_visibility="collapsed")
            else:
                for label in labels:
                    st.checkbox(label, key=f"ans_{q['id']}_{label}")
            
            st.markdown("<br>", unsafe_allow_html=True)

        submit_btn = st.form_submit_button("🔒 SUBMIT JAWABAN")
        if submit_btn:
            st.session_state.submitted = True
            st.rerun()

else:
    # --- HASIL ---
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
            # Logic checkbox simplifikasi
            pass # Tambahkan logika multiple choice sesuai kebutuhan
            
    st.balloons()
    st.markdown(f"<h2 style='text-align:center'>Skor Akhir: {score}/{total}</h2>", unsafe_allow_html=True)
    if st.button("Ulangi"):
        st.session_state.clear()
        st.rerun()
