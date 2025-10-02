import streamlit as st
import json

# スコア説明の読み込み
with open("score_ranges.json", "r", encoding="utf-8") as f:
    score_ranges = json.load(f)

# カテゴリ定義（4つ）
categories = [
    {"id": "depth", "question": "【1】課題設定の深さ：\n\n「社会構造 × 未充足の欲求」まで掘り下げた、勝てる課題設定ができているか？"},
    {"id": "strategy", "question": "【2】勝ち筋の明確さ：\n\n「小市場の独占 → 自動拡張」までの戦略設計が組織内で共有されているか？"},
    {"id": "process", "question": "【3】プロセスの再現性：\n\n「構想 → 仮説 → 実証」のプロセスが仕組みとして確立されているか？"},
    {"id": "制度的な後押し", "question": "【4】制度的な後押し：\n\n挑戦を支える裁量・予算・評価が、制度的に整備されているか？"}
]

# ページ設定
st.set_page_config(page_title="Shiftcraft診断", layout="centered")
st.title("Shiftcraft｜新規事業診断（4カテゴリ×5段階）")

# 診断実行
scores = {}
for category in categories:
    st.markdown(f"### {category['question']}")
    
    # ▼ 各スコアの詳細説明を表示
    if category["id"] in score_ranges:
        for score in range(1, 6):
            explanation = score_ranges[category["id"]].get(str(score), "")
            st.markdown(f"- **{score}点**：{explanation}")

    # ▼ スコア入力（ラジオボタン）
    selected_score = st.radio("選択肢を選んでください", [1, 2, 3, 4, 5], key=category["id"])
    scores[category["id"]] = selected_score

# 結果表示
if st.button("診断結果を見る"):
    st.subheader("診断結果（あなたのスコア）")
    total_score = sum(scores.values())
    for cat_id, score in scores.items():
        st.write(f"・{cat_id}：{score}点")
    st.markdown(f"### ✅ 合計スコア：{total_score} / 20")

    # コメント例（任意で強化可）
    if total_score <= 8:
        st.warning("全体的に改善の余地があります。特に構想プロセスや制度面の整備が求められます。")
    elif total_score <= 14:
        st.info("一部に強みがありますが、再現性やスケール戦略の明確化が必要です。")
    else:
        st.success("良好な状態です。この調子で組織全体への展開を検討しましょう。")

# 利用者向けの補足
with st.expander("この診断について"):
    st.markdown("""
このアプリは、Shiftcraftが提唱する**「成功確率を高める4要素」**を自己診断するためのツールです：

1. 課題設定の深さ  
2. 勝ち筋の明確さ  
3. プロセスの再現性  
4. 制度的な後押し  

それぞれ5段階評価でスコア化し、全体のバランスと課題を可視化します。
""")

