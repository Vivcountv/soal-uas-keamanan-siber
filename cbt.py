import streamlit as st
import requests
import time

API = "http://localhost:5000"

JUMLAH_SOAL = 20
DURASI_MENIT = 30

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
    st.session_state.answers = {}

elapsed = time.time() - st.session_state.start_time
sisa = max(DURASI_MENIT*60 - elapsed, 0)

menit = int(sisa // 60)
detik = int(sisa % 60)

st.sidebar.title("⏱ Timer CBT")
st.sidebar.metric("Sisa Waktu", f"{menit:02}:{detik:02}")

if sisa <= 0:
    st.warning("Waktu habis! Jawaban otomatis dikirim.")
    res = requests.post(f"{API}/submit", json={"answers": st.session_state.answers})
    st.json(res.json())
    st.stop()

if "questions" not in st.session_state:
    res = requests.get(f"{API}/questions?n={JUMLAH_SOAL}")
    st.session_state.questions = res.json()

for q in st.session_state.questions:
    st.subheader(q["question"])

    qid = str(q["id"])

    if q["type"] == "single":
        ans = st.radio("", list(q["options"].keys()), 
                       format_func=lambda x: f"{x}. {q['options'][x]}", 
                       key=qid)
        st.session_state.answers[qid] = [ans]

    else:
        selected = []
        for k, v in q["options"].items():
            if st.checkbox(f"{k}. {v}", key=f"{qid}_{k}"):
                selected.append(k)
        st.session_state.answers[qid] = selected

if st.button("Submit Jawaban"):
    res = requests.post(f"{API}/submit", json={"answers": st.session_state.answers})
    st.success("Hasil Ujian:")
    st.json(res.json())
