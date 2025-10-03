import streamlit as st
import json
from score_logic import calculate_scores  # get_phase_and_adviceは使わないので削除

# --- 設問読み込み ---
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# --- 評価コメント読み込み ---
with open("score_comment_ranges.json", "r", encoding="utf-8") as f:
    score_comments = json.load(f)

st.set_page_config(page_title="構想ボトルネック診断", layout="centered")
st.title("構想ボトルネック診断")
st.markdown("① 各項目を自己診断してください（1〜5点）")

scores = {}

# --- 設問表示 ---
# questionsは辞書なので.items()で回す
for category, content in questions.items():
    st.subheader(f"【{category}】")
    st.write(content["question"])
    # optionsは辞書なので、キーが"1","2","3"...の形
    selected = st.radio(
        label="",
        options=list(content["options"].keys()),
        format_func=lambda x: f"{x}：{content['options'][x]}",
        key=category
    )
    scores[category] = int(selected)

if st.button("診断する"):
    total_score = calculate_scores(list(scores.values()))
    st.write("合計スコア：", total_score)
    # コメントなどはここに追記可能
