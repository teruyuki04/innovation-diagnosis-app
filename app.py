# -*- coding: utf-8 -*-
import streamlit as st
import json

# ページ設定
st.set_page_config(page_title="イノベーション診断アプリ", layout="centered")
st.title("🧭 イノベーション診断アプリ")

# ファイル読み込み
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

with open("score_ranges.json", "r", encoding="utf-8") as f:
    score_descriptions = json.load(f)

with open("score_comment_ranges.json", "r", encoding="utf-8") as f:
    comment_ranges = json.load(f)

# 回答保存用
scores = {}

st.markdown("以下の4項目について、1〜5点で現在の状態を評価してください。")

# 質問ごとに表示
for item in questions:
    category = item["category"]
    question = item["question"]
    st.markdown(f"### 【{category}】")
    st.write(question)

    # 選択肢の説明を取得
    options = score_descriptions.get(category, {})

    # 選択肢表示（1〜5）
    score = st.radio(
        "スコアを選んでください",
        options=[1, 2, 3, 4, 5],
        key=category,
        format_func=lambda x: f"{x}：{options.get(str(x), '')}"
    )

    scores[category] = score
    st.markdown("---")

# 診断結果表示
if st.button("診断結果を見る"):
    st.header("🧾 診断結果")

    # 合計スコア計算
    total_score = sum(scores.values())
    st.markdown(f"### あなたの合計スコア：**{total_score} / 20**")

    # 合計スコアによるタイプ診断
    for entry in comment_ranges:
        if entry["min"] <= total_score <= entry["max"]:
            st.markdown(f"#### 🎯 あなたの診断タイプ：**{entry['title']}**")
            st.markdown(f"{entry['message']}")
            break

    # 各カテゴリのスコアと説明も出す
    st.markdown("### 各カテゴリのスコア内訳")
    for cat, score in scores.items():
        desc = score_descriptions.get(cat, {}).get(str(score), "")
        st.write(f"- **{cat}：{score}点** … {desc}")
