import streamlit as st
import json
from score_logic import calculate_scores

# ページ設定
st.set_page_config(page_title="構想ボトルネック診断", layout="wide")

# タイトル
st.title("🌟 Shiftcraft｜構想ボトルネック診断")
st.markdown("### あなたの構想が今どの段階にある？スコアで可視化し、次の一手を示します")

# 質問読み込み
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# コメント読み込み（score_comment_ranges.json）
with open("score_comment_ranges.json", "r", encoding="utf-8") as f:
    score_comments = json.load(f)

# 回答入力
responses = {}
for category, item in questions.items():
    st.header(category)
    score = st.radio(
        item["question"],
        list(item["options"].values()),
        index=2
    )
    selected_score = list(item["options"].values()).index(score) + 1
    responses[category] = selected_score

# 診断ボタン
if st.button("スコアを診断する"):
    total_score, breakdown = calculate_scores(responses)

    st.subheader("🧮 あなたの構想スコア：")
    st.metric("合計スコア", f"{total_score} / 20")

    # コメント選定
    matched_comment = None
    for item in score_comments:
        if item["min_score"] <= total_score <= item["max_score"]:
            matched_comment = item["comment"]
            break

    # スコアに応じた段階番号
    if total_score <= 9:
        current_phase = 1
        phase_color = "#e63946"
    elif total_score <= 14:
        current_phase = 2
        phase_color = "#f4a261"
    elif total_score <= 17:
        current_phase = 3
        phase_color = "#e9c46a"
    else:
        current_phase = 4
        phase_color = "#2a9d8f"

    # フェーズ名一覧
    phases = [
        "1. 属人依存（構想不在・現場依存）",
        "2. 個別最適（点在する成功事例）",
        "3. 土台形成済（再現性と共有の始動）",
        "4. 全社展開可能（構造整備済・拡張段階）"
    ]

    # 表示：あなたの位置
    st.markdown("### 🧭 あなたの構想フェーズ（全4段階）：")
    for i, phase in enumerate(phases, start=1):
        if i == current_phase:
            st.markdown(f"<div style='color:{phase_color}; font-weight:bold;'>🟢 {phase} ← あなたはここ</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"⬜ {phase}")

    # フェーズの詳細コメント
    st.markdown(f"<div style='padding:1em; background-color:#f9f9f9; border-left: 5px solid {phase_color};'><pre style='white-space: pre-wrap;'>{matched_comment}</pre></div>", unsafe_allow_html=True)

    # スコア内訳
    with st.expander("🗂 スコア内訳を表示"):
        for category, score in breakdown.items():
            st.write(f"{category}: {score}点")




