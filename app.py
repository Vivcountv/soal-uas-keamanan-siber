import streamlit as st
import json
import random
import time
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CBT Keamanan Siber",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. DUMMY DATA (Fallback jika file json tidak ada) ---
# Ini agar kode bisa langsung jalan saat dicoba tanpa file eksternal
DEFAULT_QUESTIONS = [
    {
        "id": 1,
        "type": "single",
        "question": "Protokol manakah yang digunakan untuk mengamankan komunikasi web?",
        "options": {"A": "HTTP", "B": "HTTPS", "C": "FTP", "D": "SMTP"},
        "correct": ["B"]
    },
    {
        "id": 2,
        "type": "multiple",
        "question": "Manakah dari berikut ini yang termasuk jenis malware? (Pilih dua)",
        "options": {"A": "Firewall", "B": "Trojan", "C": "Ransomware", "D": "Ethernet"},
        "correct": ["B", "C"]
    },
    {
        "id": 3,
        "type": "single",
        "question": "Apa kepanjangan dari CIA Triad dalam keamanan informasi?",
        "options": {"A": "Confidentiality, Integrity, Availability", "B": "Control, Intelligence, Authorization", "C": "Cyber, Internet, Access", "D": "Central, Information, Agency"},
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

# --- 4. CSS CLEAN & SIMPLE ---
st.markdown("""
<style>
    /* Font & Base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background-color: #f8f9fa; /* Light Grey Background */
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
        margin-bottom: 20px;
        border: 1px solid #e9ecef;
    }

    /* Typography */
    h1 {
        color: #1a202c;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .question-text {
        font-size: 1.15rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
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

    /* Tombol Submit */
    .stButton > button {
        background-color: #3182ce; /* Corporate Blue */
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        width: 100%;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background-color: #2c5282;
    }

    /* Score Box */
    .score-box {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 5. SESSION STATE MANAGEMENT ---
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
    # Randomize questions once
    st.session_state.quiz_data = random.sample(questions, len(questions))
    # Shuffle options
    for q in st.session_state.quiz_data:
        items = list(q["options"].items())
        random.shuffle(items)
        q["shuffled_options"] = items

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# --- 6. LOGIKA TIMER (Server Side Check) ---
DURATION_SEC = 30 * 60  # 30 Menit
elapsed = time.time() - st.session_state.start_time
remaining_sec = max(0, DURATION_SEC - elapsed)

if remaining_sec <= 0 and not st.session_state.submitted:
    st.session_state.submitted = True
    st.warning("Waktu telah habis!")

# --- 7. HEADER & VISUAL TIMER (Client Side JS) ---
st.markdown("<h1>🛡️ CBT Keamanan Siber</h1>", unsafe_allow_html=True)

# Timer JavaScript (Agar tidak perlu st.rerun() terus menerus)
if not st.session_state.submitted:
    timer_html = f"""
        <div style="
            text-align: center; 
            font-family: sans-serif; 
            font-size: 1.2rem; 
            font-weight: bold; 
            color: #e53e3e; 
            background: #fff5f5; 
            padding: 10px; 
            border-radius: 10px; 
            margin-bottom: 20px;
            border: 1px solid #fed7d7;">
            ⏱️ Sisa Waktu: <span id="timer">--:--</span>
        </div>
        <script>
        var timeLeft = {int(remaining_sec)};
        var timerElem = document.getElementById('timer');
        
        var countdown = setInterval(function() {{
            if(timeLeft <= 0) {{
                clearInterval(countdown);
                timerElem.innerHTML = "WAKTU HABIS";
            }} else {{
                var m = Math.floor(timeLeft / 60);
                var s = timeLeft % 60;
                timerElem.innerHTML = m + "m " + (s < 10 ? "0" : "") + s + "s";
                timeLeft--;
            }}
        }}, 1000);
        </script>
    """
    components.html(timer_html, height=80)

# --- 8. FORM QUIZ ---
if not st.session_state.submitted:
    # Kita bungkus semua pertanyaan dalam st.form
    # Ini membuat halaman TIDAK reload setiap kali user memilih jawaban
    with st.form(key='quiz_form'):
        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"""
            <div class="question-card">
                <span class="question-badge">Soal {i + 1}</span>
                <div class="question-text">{q['question']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Opsi Jawaban
            labels = [f"{k}. {v}" for k, v in q["shuffled_options"]]
            
            if q["type"] == "single":
                st.radio(
                    "Pilih Jawaban:", 
                    labels, 
                    key=f"ans_{q['id']}", 
                    index=None, 
                    label_visibility="collapsed"
                )
            else:
                st.markdown("<p style='font-size:0.9rem; color:#666; margin-bottom:5px;'>Pilih semua yang benar:</p>", unsafe_allow_html=True)
                for label in labels:
                    st.checkbox(label, key=f"ans_{q['id']}_{label}")

        st.markdown("---")
        submit_btn = st.form_submit_button("🔒 KUNCI & KIRIM JAWABAN")
        
        if submit_btn:
            st.session_state.submitted = True
            st.rerun()

# --- 9. HASIL & PENILAIAN ---
else:
    # Hitung Skor
    score = 0
    total_q = len(st.session_state.quiz_data)
    results = []

    for q in st.session_state.quiz_data:
        correct_keys = q["correct"]
        user_correct = False
        user_response = []

        if q["type"] == "single":
            # Ambil jawaban user dari session state
            ans_key = f"ans_{q['id']}"
            if ans_key in st.session_state and st.session_state[ans_key]:
                selected_opt = st.session_state[ans_key].split(".")[0] # Ambil "A", "B", dll
                user_response = [selected_opt]
                if selected_opt in correct_keys:
                    score += 1
                    user_correct = True
        
        else: # Multiple choice
            # Cek manual checkbox
            selected_opts = []
            for k, v in q["shuffled_options"]:
                cb_key = f"ans_{q['id']}_{k}. {v}"
                if st.session_state.get(cb_key, False):
                    selected_opts.append(k)
            
            user_response = selected_opts
            # Logika penilaian: Harus persis sama (bisa diubah ke partial score jika mau)
            if set(selected_opts) == set(correct_keys):
                score += 1
                user_correct = True
            # Partial score logic (opsional): score += len(set(selected_opts) & set(correct_keys)) / len(correct_keys)

        results.append({
            "question": q["question"],
            "user_correct": user_correct,
            "correct_ans": correct_keys,
            "user_ans": user_response
        })

    final_score = (score / total_q) * 100

    # Tampilan Hasil
    st.markdown(f"""
    <div class="score-box">
        <h2 style="color: #2d3748;">Hasil Ujian</h2>
        <div style="font-size: 3rem; font-weight: 700; color: {'#38a169' if final_score >= 70 else '#e53e3e'};">
            {final_score:.0f}
        </div>
        <p style="color: #718096;">Skor Akhir Anda</p>
    </div>
    """, unsafe_allow_html=True)

    if final_score >= 70:
        st.success("Selamat! Anda lulus kompetensi ini.")
    else:
        st.error("Maaf, skor Anda belum memenuhi standar kelulusan.")

    with st.expander("📄 Lihat Pembahasan Detail"):
        for i, res in enumerate(results):
            color = "#c6f6d5" if res['user_correct'] else "#fed7d7"
            icon = "✅" if res['user_correct'] else "❌"
            
            st.markdown(f"""
            <div style="background: {color}; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                <strong>{i+1}. {res['question']}</strong><br>
                <span style="font-size:0.9rem">Jawaban Anda: {res['user_ans']} {icon}</span><br>
                <span style="font-size:0.9rem; color:#2f855a">Kunci Jawaban: {res['correct_ans']}</span>
            </div>
            """, unsafe_allow_html=True)
            
    if st.button("🔄 Kerjakan Ulang"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
