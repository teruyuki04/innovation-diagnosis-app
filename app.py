import streamlit as st
import json

# JSON読み込み
with open("questions.json", "r", encoding="utf-8") as f:
    ranges = json.load(f)

st.title("✅【構想プロセスのボトルネック診断チェックリスト】")

st.write("""
このチェックリストは、次の柱となる事業がなぜ生まれないのか──  
その原因を「構造的なボトルネック」として可視化するためのものです。
""")

st.markdown("### 🔢 評価基準（共通）")
st.write("""
- 1点：まったくできていない／仕組みがない  
- 2点：一部にはあるが、属人化・偶発的  
- 3点：仕組みはあるが、全社的には運用されていない  
- 4点：実践と改善のサイクルが定着している  
- 5点：全社に再現可能な仕組みとして標準化されている
""")

questions = [
    {
        "title": "【1】課題設定の深さ",
        "question": "「社会構造 × 未充足の欲求」まで掘り下げた、勝てる課題設定ができているか？"
    },
    {
        "title": "【2】勝ち筋の明確さ",
        "question": "「小市場の独占 → 自動拡張」までの戦略設計が組織内で共有されているか？"
    },
    {
        "title": "【3】プロセスの再現性",
        "question": "「構想 → 仮説 → 実証」のプロセスが仕組みとして確立されているか？"
    },
    {
        "title": "【4】制度的な後押し",
        "question": "挑戦を支える裁量・予算・評価が、制度的に整備されているか？"
    }
]

scores = []
for q in questions:
    st.markdown(f"### {q['title']}")
    st.write(q["question"])
    score = st.radio("選択肢を選んでください", [1, 2, 3, 4, 5], key=q['title'])
    scores.append(score)

total_score = sum(scores)

st.markdown("---")
st.markdown("## 📝 診断結果")
st.write(f"**あなたの合計スコア： {total_score} / 20**")

# 該当レンジを判定
matched = None
for r in ranges:
    if r["min"] <= total_score <= r["max"]:
        matched = r
        break

if matched:
    st.markdown(f"### 🟢 {matched['title']}")
    st.write(matched['description'])
    st.markdown("**次の一歩（例）**")
    for step in matched['next_steps']:
        st.write(f"- {step}")

    # 4段階モデル図（簡易バージョン）
    st.markdown("---")
    st.markdown("### あなたの位置（4段階モデル）")
    options = ["属人依存", "個別最適", "土台構築", "全社展開"]
    display = ""
    for opt in options:
        if opt == matched['label']:
            display += f"🟩 **{opt}** ← ★あなたはここ\n\n"
        else:
            display += f"⬜ {opt}\n\n"
    st.markdown(display)
