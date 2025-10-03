import streamlit as st
import json
import pandas as pd
from score_logic import calculate_scores, get_phase_and_advice

# ファイル読み込み関数
@st.cache_data
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# データ読み込み
questions = load_json("questions.json")
score_comments = load_json("score_comment_ranges.json")

# タイトル
st.title("構想ボトルネック診断")

# 質問表示と回答取得
scores = {}
for category in questions:
    st.subheader(f"【{category}】")
    selected = st.radio(
        questions[category]["question"],
        options=list(questions[category]["options"].keys()),
        format_func=lambda x: f"{x}：{questions[category]['options'][x]}",
        key=category
    )
    scores[category] = int(selected)

# 診断ボタン
if st.button("診断する"):
    total_score, comment = calculate_scores(scores, score_comments)
    phase, advice = get_phase_and_advice(total_score)

    st.markdown("### 🔢 総合スコア")
    st.write(f"{total_score} 点")

    st.markdown("### 🧭 現在のフェーズ")
    st.write(phase)

    st.markdown("### 💬 フェーズ解説")
    st.write(advice)

    st.markdown("### 📌 コメント")
    st.write(comment)
