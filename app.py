import streamlit as st
import json
import random
import time

with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

st.set_page_config(page_title="CBT Siber", layout="centered")

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "answers" not in st.session_state:
    st.session_state.answers = {}

DURATION = 60 * 30  # 30 menit
remaining = DURATION - int(time.time() - st.session_state.start_time)

if remaining <= 0:
    st.error("Waktu habis!")
    st.stop()

st.title("CBT Keamanan Siber")
st.info(f"Sisa waktu: {remaining//60}:{remaining%60:02d}")

random.shuffle(questions)

score = 0

for q in questions:
    st.write(q["question"])
    opts = list(q["options"].items())
    random.shuffle(opts)

    if q["type"] == "single":
        ans = st.radio("", [f"{k}. {v}" for k,v in opts], key=q["id"])
        st.session_state.answers[q["id"]] = ans[0]
    else:
        ans = st.multiselect("", [f"{k}. {v}" for k,v in opts], key=q["id"])
        st.session_state.answers[q["id"]] = [x[0] for x in ans]

if st.button("Submit"):
    for q in questions:
        user = st.session_state.answers.get(q["id"], [])
        correct = q["correct"]

        if q["type"] == "single":
            if user in correct:
                score += 1
        else:
            score += len(set(user) & set(correct)) / len(correct)

    st.success(f"Skor akhir: {round(score,2)} / {len(questions)}")
