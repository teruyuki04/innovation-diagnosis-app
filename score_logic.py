# score_logic.py

def calculate_total_score(answers):
    return sum(int(score) for score in answers.values())

def get_comment_for_score(score, score_ranges):
    for item in score_ranges["score_ranges"]:
        if item["min"] <= score <= item["max"]:
            return item["comment"]
    return "該当する診断コメントが見つかりませんでした。"
