# force rebuild
import streamlit as st
import json
import pandas as pd
from score_logic import calculate_scores

st.set_page_config(page_title="イノベーション診断アプリ", layout="wide")
st.title("🧭 イノベーション診断アプリ")

# 質問の読み込み
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# コメント範囲の読み込み
with open("score_comment_ranges.json", "r", encoding="utf-8") as f:
    comment_ranges = json.load(f)

# チェックリストの読み込み
with open("diagnosis_checklist.txt", "r", encoding="utf-8") as f:
    checklist_items = [line.strip() for line in f.readlines() if line.strip()]

st.header("✅ チェックリスト（初期確認）")
checklist_responses = []
for item in checklist_items:
    checked = st.checkbox(item)
    checklist_responses.append((item, checked))

st.divider()
st.header("📝 診断質問")
responses = {}
for category in questions:
    st.subheader(category["category"])
    for q in category["questions"]:
        key = f'{category["category"]}_{q["id"]}'
        responses[key] = st.slider(q["text"], 1, 5, 3)

if st.button("診断実行"):
    st.subheader("📊 診断結果")
    category_scores, total_score = calculate_scores(questions, responses)

    st.write(f"### 🧮 総合スコア: {total_score} 点（100点満点）")

    # コメント表示
    for entry in comment_ranges["total_score"]:
        if entry["min"] <= total_score <= entry["max"]:
            st.info(f"💬 総評: {entry['comment']}")
            break

    # カテゴリ別表示
    st.write("### 🗂 カテゴリ別スコア")
    for category, score in category_scores.items():
        st.write(f"#### {category}: {score} 点")
        for entry in comment_ranges["categories"].get(category, []):
            if entry["min"] <= score <= entry["max"]:
                st.caption(f"💡 {entry['comment']}")
                break

    st.divider()
    st.subheader("📌 実行前チェック再掲")
    for item, checked in checklist_responses:
        st.write(f"{'✅' if checked else '⬜️'} {item}")
