import streamlit as st
import json
import os
import importlib.util
from score_logic import calculate_total_score, get_comment_for_score

# ページ設定
st.set_page_config(page_title="構想ボトルネック診断", layout="centered")
st.title("🧠 構想ボトルネック診断")
st.write("以下の4項目について、あなたの組織の現状に最も近いものを選んでください。")

# JSONファイルの読み込み関数
@st.cache_data
def load_json_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# データ読み込み
questions = load_json_file("questions.json")
score_ranges = load_json_file("score_comment_ranges.json")

# ユーザー入力の取得
user_answers = {}

for category, content in questions.items():
    st.subheader(category)
    st.write(content["question"])
    options = content["options"]
    user_answers[category] = st.radio(
        "選択肢を選んでください",
        options=list(options.keys()),
        format_func=lambda x: f"{x}. {options[x]}",
        key=category,
    )

# 診断処理
if st.button("診断する"):
    total_score = calculate_total_score(user_answers)
    comment = get_comment_for_score(total_score, score_ranges)

    st.markdown("---")
    st.subheader("診断結果")
    st.metric(label="合計スコア", value=f"{total_score} 点")
    st.write(comment)
    st.markdown("---")

    # スコアに応じた段階を表示（図は後ほど追加可能）
    if total_score <= 8:
        st.warning("🟥 フェーズ1：構想以前（ボトルネックが大きい状態）")
    elif total_score <= 14:
        st.info("🟨 フェーズ2：構想試行（挑戦の芽がある）")
    elif total_score <= 18:
        st.success("🟩 フェーズ3：構想推進（成功確率が高まる）")
    else:
        st.balloons()
        st.success("🌟 フェーズ4：構想飛躍（スケール可能な構想）")

    st.markdown("📊 図解による位置づけ（今後追加予定）")

