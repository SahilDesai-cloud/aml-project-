import pandas as pd


def simulated_defense_recovery(
    baseline_results: pd.DataFrame,
    poisoned_results: pd.DataFrame,
    recovery_factor: float = 0.6
) -> pd.DataFrame:
    """
    Simulate recovery from poisoned performance toward baseline.
    """
    baseline_results = baseline_results.copy()
    poisoned_results = poisoned_results.copy()

    baseline_results["Model"] = baseline_results["Model"].astype(str).str.strip()
    poisoned_results["Model"] = poisoned_results["Model"].astype(str).str.strip()

    defense_rows = []

    for model in ["Random Forest", "AdaBoost", "XGBoost"]:
        base = baseline_results[baseline_results["Model"] == model].iloc[0]
        poison = poisoned_results[poisoned_results["Model"] == model].iloc[0]

        defense_rows.append({
            "Scenario": "After Defense",
            "Model": model,
            "Precision": poison["Precision"] + recovery_factor * (base["Precision"] - poison["Precision"]),
            "Recall": poison["Recall"] + recovery_factor * (base["Recall"] - poison["Recall"]),
            "F1 Score": poison["F1 Score"] + recovery_factor * (base["F1 Score"] - poison["F1 Score"]),
            "PR-AUC": poison["PR-AUC"] + recovery_factor * (base["PR-AUC"] - poison["PR-AUC"]),
            "False Positives": int(round(
                poison["False Positives"] - recovery_factor * (poison["False Positives"] - base["False Positives"])
            )),
            "False Negatives": int(round(
                poison["False Negatives"] - recovery_factor * (poison["False Negatives"] - base["False Negatives"])
            ))
        })

    return pd.DataFrame(defense_rows)