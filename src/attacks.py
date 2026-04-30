import numpy as np


def label_flipping_attack(y_train, poison_rate: float = 0.20, random_state: int = 42):
    """
    Flip a fraction of labels in the training set.
    """
    np.random.seed(random_state)

    y_train_poisoned = y_train.copy()
    n_poison = int(len(y_train_poisoned) * poison_rate)

    poison_indices = np.random.choice(
        y_train_poisoned.index,
        size=n_poison,
        replace=False
    )

    y_train_poisoned.loc[poison_indices] = 1 - y_train_poisoned.loc[poison_indices]

    return y_train_poisoned, poison_indices