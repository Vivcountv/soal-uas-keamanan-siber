from docx import Document
import json
import re

doc = Document("sesuaikan lagi pertanyaan.docx")

questions = []
qid = 1

pattern = r"([A-E])\.\s*"

for p in doc.paragraphs:
    text = p.text.strip()
    if not text:
        continue

    # hanya proses paragraf yg mengandung A.
    if "A." in text and "B." in text:
        # hapus nomor soal
        text = re.sub(r"^\d+\.*\s*", "", text)

        parts = re.split(pattern, text)
        question = parts[0].strip()

        options = {}
        correct = []

        for i in range(1, len(parts), 2):
            key = parts[i]
            val = parts[i+1].strip()

            if "✅" in val:
                correct.append(key)
                val = val.replace("✅", "").strip()

            options[key] = val

        q_type = "multiple" if len(correct) > 1 else "single"

        questions.append({
            "id": qid,
            "question": question,
            "options": options,
            "correct": correct,
            "type": q_type,
            "weight": 1
        })
        qid += 1

with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print("Total soal:", len(questions))
