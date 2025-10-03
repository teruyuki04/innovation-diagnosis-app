import streamlit as st
import json
from score_logic import calculate_scores
from PIL import Image

# ページ設定
st.set_page_config(page_title="Shiftcraft 構想ボトルネック診断", layout="wide")

# タイトル
st.title("🌟 Shiftcraft｜構想ボトルネック診断")
st.markdown("### あなたの構想が今どの段階にある？スコアで可視化し、次の一手を示します")

# 質問ファイル読み込み
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# コメント範囲（score_comment_ranges.json）を読み込み
with open("score_comment_ranges.json", "r", encoding="utf-8") as f:
    score_comments = json.load(f)

# 回答を格納する辞書
responses = {}

# 質問UIの生成
for category, item in questions.items():
    st.header(category)
    score = st.radio(
        item["question"],
        list(item["options"].values()),
        index=2
    )
    # 選択された選択肢のスコア（1～5）を保存
    selected_score = list(item["options"].values()).index(score) + 1
    responses[category] = selected_score

# 診断ボタンが押されたら
if st.button("スコアを診断する"):
    total_score, breakdown = calculate_scores(responses)

    st.subheader("🧮 あなたの構想スコア：")
    st.metric("合計スコア", f"{total_score} / 20")

    # スコア範囲に応じてコメントを表示
    matched_comment = None
    for item in score_comments:
        if item["min_score"] <= total_score <= item["max_score"]:
            matched_comment = item["comment"]
            break

    # 色付きラベルの判定
    if total_score <= 9:
        phase_color = "#e63946"  # 赤
    elif total_score <= 14:
        phase_color = "#f4a261"  # オレンジ
    elif total_score <= 17:
        phase_color = "#e9c46a"  # 黄
    else:
        phase_color = "#2a9d8f"  # 緑

    # 表示ブロック
    st.markdown(f"<h3 style='color:{phase_color}'>🧭 フェーズ診断：{matched_comment.splitlines()[0]}</h3>", unsafe_allow_html=True)
    st.markdown(f"<div style='padding:1em; background-color:#f9f9f9; border-left: 5px solid {phase_color};'><pre style='white-space: pre-wrap;'>{matched_comment}</pre></div>", unsafe_allow_html=True)

    # スコア内訳表示
    with st.expander("🗂 スコア内訳を表示"):
        for category, score in breakdown.items():
            st.write(f"{category}: {score}")




