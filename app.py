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
for category, items in questions.items():
    st.header(category)
    for item in items:
        responses[item] = st.slider(item, 1, 5, 3)

# スコア計算と結果表示
if st.button("スコアを診断する"):
    total_score, breakdown = calculate_scores(responses)

    # スコア表示
    st.subheader("🧮 あなたの構想スコア：")
    st.metric("合計スコア", f"{total_score} / 20")

    # スコアに応じたフェーズと色の割り当て
    if total_score <= 8:
        phase = "🟥 属人依存の危機"
        color = "red"
    elif total_score <= 12:
        phase = "🟧 部分最適"
        color = "orange"
    elif total_score <= 16:
        phase = "🟨 飛躍準備"
        color = "gold"
    else:
        phase = "🟩 拡張の好機"
        color = "green"

    # 色付き表示
    st.markdown(f"<h3 style='color:{color}'>現在のフェーズ：{phase}</h3>", unsafe_allow_html=True)

    # コメント表示
    comment = score_comments.get(str(total_score), "該当するコメントが見つかりませんでした。")
    st.markdown(f"### 💬 解釈と次の一手\n{comment}")

    # スコア内訳表示（オプション）
    with st.expander("スコア内訳を表示"):
        for category, score in breakdown.items():
            st.write(f"{category}: {score}")



