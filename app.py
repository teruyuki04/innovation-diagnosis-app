# force rebuild

import streamlit as st
import json
from score_logic import calculate_scores

# 設問読み込み
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# 評価コメント読み込み
with open("score_comment_ranges.json", "r", encoding="utf-8") as f:
    score_comments = json.load(f)

st.set_page_config(page_title="構想ボトルネック診断", layout="centered")
st.title("🧭 構想ボトルネック診断")
st.markdown("経営構想を阻むボトルネックを可視化し、次の一手を明確にする自己診断ツールです。")

# 入力スコア保持
scores = {}

# 設問表示
for category in questions:
    st.subheader(f"【{category['category']}】")
    score = st.radio(
        label=category["description"],
        options=[(i+1, option) for i, option in enumerate(category["options"])],
        format_func=lambda x: f"{x[0]}：{x[1]}",
        key=category["category"]
    )
    scores[category["category"]] = score[0]

# 診断ボタン
if st.button("診断する"):
    total_score = calculate_scores(list(scores.values()))
    st.subheader(f"🎯 総合スコア：{total_score} 点（最大20点）")

    # コメント判定
    matched_comment = next(
        (c for c in score_comments if c["min"] <= total_score <= c["max"]),
        None
    )

    if matched_comment:
        st.markdown(f"### 🧭 現在のフェーズ：{matched_comment['phase']}")
        st.markdown(f"**{matched_comment['title']}**")
        st.info(matched_comment["comment"])

        # SVG図表示（任意）
        try:
            with open("assets/phase_chart.svg", "r", encoding="utf-8") as f:
                svg = f.read()
            st.components.v1.html(svg, height=400)
        except FileNotFoundError:
            st.warning("※フェーズ図が未設定です。`assets/phase_chart.svg` を追加してください。")
    else:
        st.error("診断コメントが見つかりませんでした。")
