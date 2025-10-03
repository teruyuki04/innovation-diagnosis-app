import streamlit as st
import json
from score_logic import calculate_scores  # スコア計算ロジックを読み込む
from PIL import Image

# ページ設定
st.set_page_config(page_title="Shiftcraft 構想ボトルネック診断", layout="wide")

# タイトル
st.title("🧠 Shiftcraft | 構想ボトルネック診断")
st.markdown("### あなたの構想は今どの段階にある？スコアで可視化し、次の一手を示します")

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
        responses[item["question"]] = st.radio(
            item["question"],
            [f"{i+1}: {desc}" for i, desc in enumerate(item["choices"])],
            index=2,  # デフォルトは3番目
            key=item["question"]
        )

# 診断ボタン押下後
if st.button("診断する"):
    total_score, comment = calculate_scores(responses, score_comments)

    st.write("### 診断結果")
    st.write(f"総合スコア: {total_score}点")

    # スコアに応じて色付きメッセージを表示
    if total_score <= 9:
        st.warning("🟥 フェーズ1：構造不在・属人依存の危機ゾーン")
    elif total_score <= 14:
        st.info("🟧 フェーズ2：取り組みのムラ・部分最適ゾーン")
    elif total_score <= 17:
        st.success("🟨 フェーズ3：構想の土台あり・飛躍準備ゾーン")
    else:
        st.balloons()
        st.success("🟩 フェーズ4：構造化・制度化フェーズ（拡張の好機）")

    # コメント（詳細アドバイス）
    st.markdown("### 📝 コメント")
    st.write(comment)



