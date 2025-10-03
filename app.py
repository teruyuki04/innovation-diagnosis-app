import streamlit as st
import json
from score_logic import calculate_scores

# エラー回避のために、日本語を含まないタイトルに変更
st.set_page_config(page_title="Shiftcraft Diagnosis", layout="centered")

st.title("🧠 Shiftcraft｜構想ボトルネック診断")

# 質問読み込み
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# スコアリングUI
st.header("📋 自己診断チェック")
scores = {}
for question in questions:
    score = st.radio(
        f"{question['category']}｜{question['question']}",
        question["choices"],
        key=question["id"],
        index=2
    )
    scores[question["id"]] = question["choices"].index(score) + 1

# 結果表示
if st.button("✅ 診断する"):
    total_score, comment = calculate_score_and_comment(scores)

    st.markdown("---")
    st.subheader("🧾 診断結果")

    # スコアに応じた段階を表示
    if total_score <= 8:
        st.warning("🟧 フェーズ1：構想以前（ボトルネックが大きい状態）")
    elif total_score <= 14:
        st.info("🟨 フェーズ2：構想試行（挑戦の芽がある）")
    elif total_score <= 18:
        st.success("🟩 フェーズ3：構想進展（成功確率が高まる）")
    else:
        st.balloons()
        st.success("🌟 フェーズ4：構想飛躍（スケール可能な構想）")

    st.markdown("📊 図解による位置づけ（今後追加予定）")

    st.markdown("---")
    st.write(comment)


