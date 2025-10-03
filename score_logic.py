def calculate_scores(scores, score_comments):
    total_score = sum(scores.values())

    comment = ""
    for item in score_comments:
        if item["min_score"] <= total_score <= item["max_score"]:
            comment = item["comment"]
            break

    return total_score, comment

def get_phase_and_advice(score):
    if score <= 8:
        return "❶ 構想未満フェーズ", "課題の質や構想の立て方に抜本的な見直しが必要です。"
    elif score <= 12:
        return "❷ 幻惑の森フェーズ", "見えているようで見えていない『構想の盲点』があります。問いの深掘りが必要です。"
    elif score <= 16:
        return "❸ 死の谷フェーズ", "構想の芽はありますが、制度・組織・プロセスの詰まりを超える仕掛けが必要です。"
    else:
        return "❹ ダーウィンの海フェーズ", "構想の再現性が高まってきています。スケールに向けた仕組み化・連携強化が重要です。"
