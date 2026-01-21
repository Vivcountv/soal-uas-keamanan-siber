import streamlit as st
import json
import random
import time
from datetime import timedelta

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Page config
st.set_page_config(
    page_title="CBT Keamanan Siber",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS untuk styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Container */
    .main .block-container {
        background: white;
        border-radius: 20px;
        padding: 2rem 3rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Title */
    h1 {
        color: #667eea !important;
        text-align: center;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Timer Box */
    .timer-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem auto;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        animation: pulse 2s infinite;
        max-width: 250px;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Question Card */
    .question-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        border-left: 5px solid #667eea;
        animation: slideInLeft 0.4s ease-out;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .question-number {
        color: #667eea;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .question-text {
        font-size: 1.2rem;
        color: #333;
        font-weight: 500;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    
    /* Radio and Checkbox */
    .stRadio > label, .stMultiselect > label {
        font-weight: 600;
        color: #667eea;
        font-size: 1.1rem;
    }
    
    /* Radio options */
    .stRadio > div {
        background: white;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stRadio > div > label {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        display: block;
    }
    
    .stRadio > div > label:hover {
        border-color: #667eea;
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 0.75rem 2.5rem;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 50px;
        box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 2rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(245, 87, 108, 0.6);
    }
    
    /* Success/Error Messages */
    .stSuccess, .stError, .stInfo {
        border-radius: 10px;
        padding: 1rem;
        animation: bounceIn 0.5s ease;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Score Display */
    .score-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        margin: 2rem 0;
        animation: bounceIn 0.8s ease;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Multiselect styling */
    .stMultiselect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
    st.session_state.questions = random.sample(questions, len(questions))
    # Shuffle options for each question
    for q in st.session_state.questions:
        items = list(q["options"].items())
        random.shuffle(items)
        q["shuffled_options"] = items

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Timer
DURATION = 60 * 30  # 30 menit
remaining = DURATION - int(time.time() - st.session_state.start_time)

# Header
st.markdown("<h1>🛡️ CBT Keamanan Siber</h1>", unsafe_allow_html=True)

# Check if time is up
if remaining <= 0 and not st.session_state.submitted:
    st.error("⏰ Waktu Habis! Quiz otomatis disubmit.")
    st.session_state.submitted = True
    remaining = 0

# Timer display
minutes = remaining // 60
seconds = remaining % 60
timer_color = "#f5576c" if remaining < 300 else "#667eea"
st.markdown(f"""
<div class="timer-box" style="background: linear-gradient(135deg, {timer_color} 0%, #f093fb 100%);">
    ⏱️ {minutes:02d}:{seconds:02d}
</div>
""", unsafe_allow_html=True)

# Progress bar
if not st.session_state.submitted:
    progress = len([a for a in st.session_state.answers.values() if a]) / len(st.session_state.questions)
    st.progress(progress)
    st.markdown(f"<p style='text-align: center; color: #667eea; font-weight: 600;'>Progress: {int(progress * 100)}% ({len([a for a in st.session_state.answers.values() if a])}/{len(st.session_state.questions)} soal terjawab)</p>", unsafe_allow_html=True)

# Display questions or results
if not st.session_state.submitted:
    st.markdown("---")
    
    for idx, q in enumerate(st.session_state.questions):
        st.markdown(f"""
        <div class="question-card">
            <div class="question-number">📝 Soal {idx + 1}</div>
            <div class="question-text">{q['question']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if q["type"] == "single":
            options = [f"{k}. {v}" for k, v in q["shuffled_options"]]
            answer = st.radio(
                "Pilih satu jawaban:",
                options,
                key=f"q_{q['id']}",
                index=None
            )
            if answer:
                st.session_state.answers[q["id"]] = answer[0]
            
        else:  # multiple choice
            options = [f"{k}. {v}" for k, v in q["shuffled_options"]]
            answers = st.multiselect(
                "Pilih satu atau lebih jawaban:",
                options,
                key=f"q_{q['id']}"
            )
            st.session_state.answers[q["id"]] = [ans[0] for ans in answers]
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ SUBMIT JAWABAN", type="primary"):
            st.session_state.submitted = True
            st.rerun()

else:
    # Calculate score
    score = 0
    total = len(st.session_state.questions)
    
    for q in st.session_state.questions:
        user_answer = st.session_state.answers.get(q["id"], [])
        correct = q["correct"]
        
        if q["type"] == "single":
            if user_answer in correct:
                score += 1
        else:
            if isinstance(user_answer, list):
                correct_count = len(set(user_answer) & set(correct))
                score += correct_count / len(correct)
    
    # Display result
    st.balloons()
    st.markdown(f"""
    <div style="text-align: center; margin: 3rem 0;">
        <h2 style="color: #667eea;">🎉 Quiz Selesai!</h2>
        <div class="score-display">{score:.1f} / {total}</div>
        <p style="font-size: 1.5rem; color: #666;">
            Persentase: {(score/total*100):.1f}%
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grade
    percentage = (score / total) * 100
    if percentage >= 80:
        st.success("🌟 Luar Biasa! Anda sangat memahami keamanan siber!")
    elif percentage >= 60:
        st.info("👍 Bagus! Terus tingkatkan pemahaman Anda!")
    else:
        st.warning("📚 Perlu belajar lebih banyak. Jangan menyerah!")
    
    # Show answers
    with st.expander("📊 Lihat Pembahasan Jawaban"):
        for idx, q in enumerate(st.session_state.questions):
            user_answer = st.session_state.answers.get(q["id"], [])
            correct = q["correct"]
            
            st.markdown(f"**Soal {idx + 1}:** {q['question']}")
            
            if q["type"] == "single":
                is_correct = user_answer in correct
                st.markdown(f"- Jawaban Anda: **{user_answer}** {'✅' if is_correct else '❌'}")
                st.markdown(f"- Jawaban Benar: **{', '.join(correct)}**")
            else:
                if isinstance(user_answer, list):
                    correct_count = len(set(user_answer) & set(correct))
                    st.markdown(f"- Jawaban Anda: **{', '.join(user_answer) if user_answer else 'Tidak dijawab'}**")
                    st.markdown(f"- Jawaban Benar: **{', '.join(correct)}**")
                    st.markdown(f"- Skor: {correct_count}/{len(correct)} ✅")
                else:
                    st.markdown(f"- Jawaban Anda: **Tidak dijawab** ❌")
                    st.markdown(f"- Jawaban Benar: **{', '.join(correct)}**")
            
            st.markdown("---")
    
    # Retry button
    if st.button("🔄 Coba Lagi"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Auto refresh for timer (only if not submitted)
if not st.session_state.submitted and remaining > 0:
    time.sleep(1)
    st.rerun()
