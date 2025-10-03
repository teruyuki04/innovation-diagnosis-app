import streamlit as st
import json
import os
import pandas as pd
import importlib.util
import sys

# 動的に score_logic.py を読み込む（Streamlit CloudでのImportError対策）
spec = importlib.util.spec_from_file_location("score_logic", "score_logic.py")
score_logic = importlib.util.module_from_spec(spec)
sys.modules["score_logic"] = score_logic
spec.loader.exec_module(score_logic)

# ファイル一覧表示（デバッグ用）
st.write("現在のフォルダ内のファイル:", os.listdir())

# ファイル読み込み
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

with open("score_comment_ranges.json", "r", encoding="utf-8") as f:
    score_comments = json.load(f)

# アプリタイトル
st.set_page_config(page_title="構想ボトルネック診断", layout="centered")
st.title("構想ボトルネック診断")

# スコア入力
st.header("① 各項目を自己診断してください（1〜5点）")
scores = {}
for category, items in questions.items():
    st.subheader(f"【{category}】")
    for item in items:
        score = st.slider(f"{item}", min_value=1, max_value=5, key=f"{category}_{item}")
        scores[item] = score

# スコア計算
if st.button("診断する"):
    total_score, phase, advice = score_logic.calculate_scores(scores)
    comment = score_logic.get_phase_and_advice(phase, score_comments)

    st.markdown("---")
    st.subheader("② 診断結果")
    st.markdown(f"**スコア合計**: {total_score}点")
    st.markdown(f"**現在のフェーズ**: {phase}")
    st.markdown(f"**解釈と次の一手**: {comment}")
