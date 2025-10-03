import os
import sys

# app.py と同じディレクトリをモジュール探索パスに追加
sys.path.append(os.path.dirname(__file__))

import streamlit as st
import json
from score_logic import calculate_scores, get_phase_and_advice

# JSON 読み込み関数
def load_json(fn):
    path = os.path.join(os.path.dirname(__file__), fn)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_json("questions.json")
score_comments = load_json("score_comment_ranges.json")

st.set_page_config(page_title="構想ボトルネック診断", layout="centered")
st.title("🧭 構想ボトルネック診断")

# 質問表示と回答受付
answers = {}
for q in questions:
    cat = q["category"]
    text = q["question"]
    opts = q["options"]
    # options は dict mapping "1": description, etc
    choice = st.radio(f" {text}", opts.items(), format_func=lambda x: f"{x[0]}：{x[1]}", key=cat)
    # choice is tuple (key, description)
    answers[cat] = int(choice[0])

if st.button("診断する"):
    total_score, _dummy = calculate_scores(answers, score_comments)
    phase, advice = get_phase_and_advice(total_score, score_comments)

    st.subheader("🔢 総合スコア")
    st.metric(label="得点", value=f"{total_score} 点")

    st.subheader("🧭 フェーズ")
    st.write(phase)

    st.subheader("💡 アドバイス")
    st.write(advice)
