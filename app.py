import streamlit as st
import json
from score_logic import calculate_score_and_phase
from PIL import Image

st.set_page_config(page_title="構想ボトルネック診断", layout="wide")

st.title("🚥 Shiftcraft｜構想ボトルネック診断")
st.markdown("#### あなたの構想は今どの段階にある？スコアで可視化し、次の一手を示します")

with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

responses = {}

for category, items in questions.items():
    st.header(category)
    for item in items:
        responses[item["question"]] = st.radio(
            item["question"],
            [f"{i+1}：{desc}" for i, desc in enumerate(item["choices"])],
            index=2,
            key=item["question"]
        )

if st.button("診断する"):
    total_score, phase_label = calculate_score_and_phase(responses)

    st.markdown(f"## 🧮 合計スコア: {total_score} 点")
    st.markdown(f"## 🧭 フェーズ分類: {phase_label}")

    image = Image.open("phase_diagram.svg")
    st.image(image, caption='現在地：構想フェーズのどこに該当するか')

    with open("score_comment_ranges.json", "r", encoding="utf-8") as f:
        comment_data = json.load(f)

    phase_colors = {
        "🟥 属人依存の危機": "#f8d7da",
        "🟧 部分最適": "#fff3cd",
        "🟨 飛躍準備": "#fff9e6",
        "🟩 拡張の好機": "#d4edda"
    }

    for phase, data in comment_data.items():
        if data["min"] <= total_score <= data["max"]:
            color = phase_colors.get(phase, "#ffffff")
            st.markdown(
                f"""
                <div style="border-left: 6px solid {color}; background-color: {color}; padding: 1em; border-radius: 6px;">
                    <h4>{phase}</h4>
                    <b>{data["title"]}</b><br>
                    <p>{data["comment"]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


