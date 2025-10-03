import streamlit as st
import json
from score_logic import calculate_scores, get_phase_and_advice

# JSONファイル読み込み
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

with open("score_comment_ranges.json", "r", encoding="utf-8") as f:
    score_ranges = json.load(f)

# アプリ本体
st.set_page_config(page_title="構想ボトルネック診断", layout="centered")
st.title("構想ボトルネック診断")

st.markdown("以下の4項目について、現在の自社の状態を自己診断してください（1〜5点）")

user_scores = {}
for section in questions:
    st.subheader(section["title"])
    for q in section["questions"]:
        user_scores[q["id"]] = st.slider(q["text"], 1, 5, 3)

# 診断実行
if st.button("診断する"):
    total_score, phase, advice = calculate_scores(user_scores, score_ranges)

    st.markdown("---")
    st.header("診断結果")
    st.write(f"🧮 合計スコア: **{total_score} / 20**")
    st.write(f"📊 現在のフェーズ: **{phase}**")
    st.markdown(f"💡 アドバイス:\n\n{advice}")
