import streamlit as st
from score_logic import interpret_score

st.set_page_config(page_title="構想プロセス診断", layout="centered")
st.title("🧭 構想プロセスのボトルネック診断")

st.write("以下の設問に答えて、あなたの組織のイノベーション構造を可視化しましょう。")

questions = {
    "【1】課題設定の深さ": "社会構造 × 未充足の欲求 まで掘り下げた課題設定ができているか？",
    "【2】勝ち筋の明確さ": "小市場の独占 → 自動拡張 の戦略が共有されているか？",
    "【3】プロセスの再現性": "構想 → 仮説 → 実証 の流れが仕組み化されているか？",
    "【4】制度的な後押し": "挑戦を支える裁量・予算・評価が制度的に整備されているか？"
}

options = [
    "1点：できていない／仕組みがない",
    "2点：属人化・偶発的に一部ある",
    "3点：あるが全社的でない",
    "4点：実践と改善が定着",
    "5点：全社で標準化"
]

score = 0

for q, desc in questions.items():
    st.subheader(q)
    st.caption(desc)
    choice = st.radio("選択肢を選んでください", options, key=q)
    score += int(choice[0])

st.markdown("---")
st.header("📊 診断結果")
st.metric("あなたの合計スコア", f"{score} / 20")
st.write(interpret_score(score))
