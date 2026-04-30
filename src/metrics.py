import pandas as pd
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    confusion_matrix
)


def evaluate_model(model, X_test, y_test, model_name: str) -> dict:
    """
    Evaluate a trained model and return metrics.
    """
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    cm = confusion_matrix(y_test, y_pred)
    fp = cm[0, 1]
    fn = cm[1, 0]

    return {
        "Model": model_name,
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1 Score": f1_score(y_test, y_pred),
        "PR-AUC": average_precision_score(y_test, y_prob),
        "False Positives": fp,
        "False Negatives": fn
    }


def build_results_dataframe(results_list: list) -> pd.DataFrame:
    """
    Convert list of dictionaries into DataFrame.
    """
    return pd.DataFrame(results_list)