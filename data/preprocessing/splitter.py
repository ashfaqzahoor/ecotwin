import pandas as pd


def chronological_split(df: pd.DataFrame, train: float = 0.7, validation: float = 0.15) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ordered = df.sort_values("observed_at").reset_index(drop=True)
    train_end = int(len(ordered) * train)
    val_end = int(len(ordered) * (train + validation))
    return ordered.iloc[:train_end], ordered.iloc[train_end:val_end], ordered.iloc[val_end:]
