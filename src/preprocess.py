from sklearn.model_selection import train_test_split


def prepare_features(df, target_col: str = "label"):
    """
    Split dataframe into X and y.
    Drops txId if present.
    """
    drop_cols = [target_col]
    if "txId" in df.columns:
        drop_cols.append("txId")

    X = df.drop(columns=drop_cols)
    y = df[target_col]
    return X, y


def split_data(X, y, test_size: float = 0.2, random_state: int = 42):
    """
    Perform stratified train-test split.
    """
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )