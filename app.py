import streamlit as st
import json
from score_logic import calculate_scores

# タイトルと説明
st.set_page_config(page_title="構想ボトルネック診断", layout="wide")
st.title("🌟 Shiftcraft｜構想ボトルネック診断")
st.write("あなたの構想が今どの段階にある？スコアで可視化し、次の一手を示します")

# 質問の読み込み
with open("questions.json", "r", encoding="utf-8") as f:
    questions_data = json.load(f)

# 質問の表示と回答収集
responses = {}
for idx, (key, question) in enumerate(questions_data.items(), start=1):
    st.subheader(f"{question['category']}")
    response = st.radio(
        question["question"],
        question["options"],
        key=key,
        index=None,
        format_func=lambda x: "　" + x  # 字下げ
    )
    if response:
        responses[key] = question["options"].index(response) + 1

# スコア計算と結果表示
if st.button("スコアを診断する") and responses:
    total, responses = calculate_scores(responses)
    
    # 結果の表示
    st.subheader("🧮 あなたの構想スコア：")
    st.write(f"合計スコア：**{total} / {len(questions_data)*5}**")

    # フェーズ判定
    if total <= 9:
        phase_text = "構想不在・属人依存の危機ゾーン"
        phase_color = "#e63946"
        phase_level = 1
    elif total <= 14:
        phase_text = "個別最適（点在する成功事例）"
        phase_color = "#f4a261"
        phase_level = 2
    elif total <= 17:
        phase_text = "土台形成済（再現性と共有の始動）"
        phase_color = "#2a9d8f"
        phase_level = 3
    else:
        phase_text = "全社展開可能（構造整備済・拡張段階）"
        phase_color = "#4caf50"
        phase_level = 4

    st.markdown(f"### 🧭 フェーズ診断： <span style='color:{phase_color}; font-weight:bold;'>■ {phase_text}</span>", unsafe_allow_html=True)

    # フェーズ一覧の中で該当箇所をハイライト表示
    st.markdown("#### あなたの構想フェーズ（全4段階）：")
    phases = [
        "1. 属人依存（構想不在・現場依存）",
        "2. 個別最適（点在する成功事例）",
        "3. 土台形成済（再現性と共有の始動）",
        "4. 全社展開可能（構造整備済・拡張段階）"
    ]

    for i, phase in enumerate(phases, start=1):
        if i == phase_level:
            st.markdown(f"🟢 <span style='color:#ff8800; font-weight:bold;'>{phase} ← あなたはここ</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"⬜ {phase}")

    # コメント読み込みと表示（フェーズに応じて）
    with open("score_comment_ranges.json", "r", encoding="utf-8") as f:
        comments_data = json.load(f)
    
    matched_comment = ""
    for item in comments_data:
        if item["min"] <= total <= item["max"]:
            matched_comment = item["comment"]
            break

    if matched_comment:
        st.markdown(f"""
        <div style="
            padding:1em;
            background-color:#fefefe;
            border-left: 5px solid {phase_color};
            color:#333333;
            font-size: 1em;
            line-height: 1.6;
            word-break: break-word;
        ">
            {matched_comment.replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)

    # 詳細スコア表示
    with st.expander("📦 スコア内訳を表示"):
        for key, val in responses.items():
            st.write(f"{questions_data[key]['category']}: {val}")




