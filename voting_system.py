# NeuroDetect - voting_system.py
# Smart Feature 2: Multi Model Voting System

import numpy as np

CLASSES = ["glioma", "meningioma", "notumor", "pituitary"]

# ─────────────────────────────────────────
# MODEL WEIGHTS
# ─────────────────────────────────────────
MODEL_WEIGHTS = {
    "SVM":     0.15,
    "RF":      0.15,
    "CNN":     0.30,
    "ResNet50": 0.40
}

# ─────────────────────────────────────────
# WEIGHTED VOTING
# ─────────────────────────────────────────
def weighted_voting(results):
    weighted  = np.zeros(4)
    tw        = 0

    for model, (label, conf, probs) in results.items():
        w          = MODEL_WEIGHTS.get(model, 0.25)
        weighted  += w * np.array(probs)
        tw        += w

    weighted   /= tw
    pred_idx    = np.argmax(weighted)
    final_label = CLASSES[pred_idx]
    final_conf  = weighted[pred_idx] * 100

    return final_label, final_conf, weighted

# ─────────────────────────────────────────
# AGREEMENT SCORE
# ─────────────────────────────────────────
def get_agreement_score(results):
    predictions = [
        label for label, conf, probs
        in results.values()
    ]
    most_common = max(
        set(predictions),
        key=predictions.count
    )
    agreement = (
        predictions.count(most_common) /
        len(predictions)
    ) * 100

    if agreement == 100:
        msg   = "✅ All models agree — Very reliable!"
        color = "#00C851"
    elif agreement >= 75:
        msg   = "✅ Strong consensus — Reliable"
        color = "#FFD700"
    elif agreement >= 50:
        msg   = "⚠️ Partial agreement — Review needed"
        color = "#FF6B00"
    else:
        msg   = "❌ Models disagree — Low reliability"
        color = "#FF0000"

    return agreement, msg, color

# ─────────────────────────────────────────
# VOTE COUNT
# ─────────────────────────────────────────
def get_vote_count(results):
    votes = {}
    for model, (label, conf, probs) in results.items():
        if label not in votes:
            votes[label] = []
        votes[label].append(model)
    return votes

# ─────────────────────────────────────────
# FULL VOTING REPORT
# ─────────────────────────────────────────
def get_voting_report(results):
    final_label, final_conf, weighted = \
        weighted_voting(results)

    agreement, msg, color = \
        get_agreement_score(results)

    votes = get_vote_count(results)

    return {
        "final_prediction": final_label,
        "final_confidence": round(final_conf, 2),
        "weighted_probs":   weighted.tolist(),
        "agreement_score":  agreement,
        "agreement_msg":    msg,
        "agreement_color":  color,
        "vote_count":       votes,
        "models_used":      list(results.keys())
    }

if __name__ == "__main__":
    # Test
    test_results = {
        "SVM":     ("glioma", 90.0,
                    [0.90, 0.05, 0.03, 0.02]),
        "RF":      ("glioma", 88.0,
                    [0.88, 0.07, 0.03, 0.02]),
        "CNN":     ("glioma", 95.0,
                    [0.95, 0.03, 0.01, 0.01]),
        "ResNet50":("glioma", 97.0,
                    [0.97, 0.02, 0.005, 0.005])
    }

    report = get_voting_report(test_results)
    print("🗳️ Voting Report Test:")
    for k, v in report.items():
        print(f"  {k}: {v}")