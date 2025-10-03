import streamlit as st
import json
from score_logic import calculate_scores

st.set_page_config(page_title="Shiftcraft: 構想ボトルネック診断", layout="centered")
st.title("構想ボトルネック診断")

# JSONデータの読み込み
with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

with open('score_comment_ranges.json', 'r', encoding='utf-8') as f:
    score_comments = json.load(f)

# スコア入力保存
scores = {}

for category, content in questions.items():
    st.subheader(f"【{category}】")
    question_text = content['question']
    options = content['options']

    score = st.radio(
        label=question_text,
        options=list(options.keys()),
        format_func=lambda x: f"{x}：{options[x]}",
        key=category
    )

    scores[category] = int(score)

# 診断ボタン
if st.button("診断する"):
    total_score, comment = calculate_scores(scores, score_comments)

    st.markdown("### 🔢 合計スコア")
    st.markdown(f"**{total_score} 点**")

    st.markdown("### 📘 フェーズ診断")

    # 色付きフェーズ分岐表示
    if total_score <= 8:
        st.warning("🟥 フェーズ1：構想以前（ボトルネックが大きい状態）")
    elif total_score <= 14:
        st.info("🟨 フェーズ2：構想試行（挑戦の芽がある）")
    elif total_score <= 18:
        st.success("🟩 フェーズ3：構想進展（成功確率が高まる）")
    else:
        st.balloons()
        st.success("🌟 フェーズ4：構想熟達（スケール可能な構想）")

    st.markdown("### 💡 コメント（全体アドバイス）")
    st.write(comment)

    st.markdown("📊 図解による位置づけ（今後追加予定）")


