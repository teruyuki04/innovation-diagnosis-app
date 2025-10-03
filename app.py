# force rebuild 20251003
# force rebuild

import streamlit as st
import json
import os
from score_logic import calculate_scores

# 設問読み込み
base_dir = os.path.dirname(__file__)

questions_path = os.path.join(base_dir, "questions.json")
with open(questions_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

# 評価コメント読み込み
score_comments_path = os.path.join(base_dir, "score_comment_ranges.json")
with open(score_comments_path, "r", encoding="utf-8") as f:
    score_comments = json.load(f)

st.set_page_config(page_title="構想ボトルネック診断", layout="centered")
st.title("🧠 構想ボトルネック診断")
st.markdown("経営構想を阻むボトルネックを可視化し、次の一手を明確にする自己診断ツールです。")

# 入力スコア保存
scores = {}

# 設問表示
for category in questions:
    st.subheader(f"【{category['category']}】")
    score = st.radio(
        label=category["description"],
        options=[(i+1, option) for i, option in enumerate(category["options"])],
        format_func=lambda x: f"{x[0]}：{x[1]}",
        key=category["category"]
    )
    scores[category["category"]] = score[0]

# スコア計算ボタン
if st.button("診断する"):
    total_score, comment = calculate_scores(scores, score_comments)

    st.markdown("---")
    st.subheader("📝 診断結果")
    st.metric("合計スコア", f"{total_score} 点")
    st.write(comment)
