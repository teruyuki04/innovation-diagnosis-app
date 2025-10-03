import streamlit as st
import json
from score_logic import calculate_scores

st.set_page_config(page_title="構想ボトルネック診断", layout="wide")

st.title("🌟 Shiftcraft | 構想ボトルネック診断")
st.markdown("あなたの構想が今どの段階にある？スコアで可視化し、次の一手を示します")

with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

responses = {}

for key, question in questions.items():
    st.subheader(f"{question.get('category', '')}")
    responses[key] = st.radio(question["question"], question["options"], key=key)

if st.button("スコアを診断する"):
    total, result = calculate_scores(responses)

    st.markdown(f"### 🧮 あなたの構想スコア：")
    st.metric(label="合計スコア", value=f"{total}/20")

    # フェーズ診断ラベル
    phase_label = result["phase"]
    phase_color = result["color"]
    comment = result["comment"]

    # フェーズインジケータ（図ではなくテキスト）
    st.markdown("---")
    st.markdown("#### 🧭 フェーズ診断：")

    levels = [
        "1. 属人依存（構想不在・現場依存）",
        "2. 個別最適（点在する成功事例）",
        "3. 土台形成済（再現性と共有の始動）",
        "4. 全社展開可能（構造整備済・拡張段階）"
    ]

    # 現在のフェーズに応じて強調表示
    for idx, level in enumerate(levels, start=1):
        if phase_label.startswith(str(idx)):
            st.markdown(f"🟢 **{level} ← あなたはここ**")
        else:
            st.markdown(f"⬜ {level}")

    st.markdown("---")
    st.markdown(f"### 📝 フェーズ診断： {phase_color} **{phase_label}**")
    st.info(comment)

    with st.expander("📂 スコア内訳を表示"):
        for key, score in result["details"].items():
            st.write(f"{key}: {score}")





