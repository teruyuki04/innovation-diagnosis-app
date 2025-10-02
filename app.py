import streamlit as st
import json

# JSON読み込み
with open("score_ranges.json", "r", encoding="utf-8") as f:
    score_ranges = json.load(f)

# アプリタイトル
st.title("🧭【構想プロセスのボトルネック診断チェックリスト】")

st.write("""
このチェックリストは、次の柱となる事業がなぜ生まれないのか――  
その原因を「構造的なボトルネック」として可視化するためのものです。
""")

# 評価基準の説明
st.markdown("### 📘 評価基準（共通）")
st.write("""
1点：まったくできていない／仕組みがない  
2点：一部にはあるが、属人的、仮説的  
3点：仕組みはあるが、全体的には浸透されていない  
4点：共通言語化され組織として蓄積している  
5点：全社に理解が浸透し構造的な仕組みとして標準化されている
""")

# 質問リスト（例）
questions = [
    {
        "title": "【1】課題設定の深さ",
        "question": "代表課題・未来起点の欲求」まで掘り下げた、勝てる課題設定ができているか？"
    },
    {
        "title": "【2】勝ち筋の明確さ",
        "question": "構想に「自社独自の勝ち筋」があるか？事業仮説の骨格が構造として描かれているか？"
    },
    {
        "title": "【3】プロセスの再現性",
        "question": "再現可能なプロセスになっているか？アブダクションや仮説検証の流れが明確か？"
    },
    {
        "title": "【4】制度的な後押し",
        "question": "挑戦を支える裁量・予算・評価が、制度的に整備されているか？"
    }
]

# 回答の受付
st.markdown("### ✅ 各質問に回答してください")
total_score = 0
max_score = len(questions) * 5

for q in questions:
    st.markdown(f"**{q['title']}**")
    st.write(q["question"])
    score = st.radio("選択肢を選んでください", [1, 2, 3, 4, 5], key=q["title"])
    total_score += score
    st.markdown("---")

# 診断結果の表示
st.markdown("## 📄 診断結果")
st.markdown(f"### あなたの合計スコア：{total_score} / {max_score}")

# メッセージ表示（スコアに応じた診断コメント）
for r in score_ranges:
    if r["min"] <= total_score <= r["max"]:
        st.markdown(f"#### 🧭 あなたの診断タイプ：{r['message']}")
        break
