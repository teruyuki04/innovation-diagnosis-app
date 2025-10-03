import sys
import os
sys.path.append(os.path.dirname(__file__))

import streamlit as st
import json

from score_logic import calculate_scores, get_phase_and_advice

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Load score comment ranges
with open("score_comment_ranges.json", "r", encoding="utf-8") as f:
    comment_ranges = json.load(f)

# UI
st.title("構想ボトルネック診断")

scores = []
for q in questions:
    score = st.radio(f"【{q['category']}】{q['question']}", q["choices"], index=2, key=q["id"])
    scores.append(int(score.split("：")[0]))  # 「5：〜」→5だけを取り出す

if st.button("診断する"):
    total_score, phase = calculate_scores(scores)
    advice = get_phase_and_advice(phase, comment_ranges)

    st.subheader("🔎 総合スコア")
    st.metric(label="合計点", value=f"{total_score} 点")

    st.subheader("🧭 現在のフェーズ")
    st.success(f"{phase}")

    st.subheader("💡 アドバイス")
    st.markdown(advice)
