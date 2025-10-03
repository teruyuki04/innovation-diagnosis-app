import streamlit as st
from score_logic import calculate_score_and_comment
import json

st.set_page_config(page_title="構想ボトルネック診断", layout="centered")

st.title("🧠 構想ボトルネック診断")
st.markdown("プロジェクトの詰まりの構造を可視化し、打ち手を即座に判断するための自己診断ツールです。")

# 質問読み込み
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

scores = {}
st.header("📝 診断スタート")

for category in questions:
    st.subheader(f"【{category['category']}】")
    for q in category["questions"]:
        score = st.radio(f"・{q['question']}", [1, 2, 3, 4, 5], horizontal=True, key=q["question"])
        scores[q["question"]] = score

# 診断ロジック呼び出し
total_score, comment, color = calculate_score_and_comment(scores)

# 結果表示
st.markdown("---")
st.header("📊 診断結果")

st.markdown(f"### あなたの構想スコア： {total_score}点（100点満点）")

color_blocks = {
    "🟥": "#FF4B4B",
    "🟧": "#FFA500",
    "🟨": "#FFD700",
    "🟩": "#2ECC71"
}
bg_color = color_blocks.get(color[:2], "#DDDDDD")

st.markdown(
    f"""
    <div style='background-color: {bg_color}; padding: 1rem; border-radius: 0.5rem;'>
        <h3 style='margin: 0;'>{color} {comment['title']}</h3>
        <p style='margin-top: 0.5rem;'>{comment['description']}</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("")

st.subheader("🧭 次の一手")
st.markdown(f"**▶ {comment['action']}**")

st.markdown("---")
st.caption("© Shiftcraft / Proudfoot Japan")



