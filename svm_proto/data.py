import csv
from typing import List, Tuple


def load_csv(path: str) -> Tuple[List[List[float]], List[int]]:
    """Load features and labels from a CSV file.

    Each row must have at least two columns. All columns are parsed as floats;
    features are all but the last column, and the label is the last column
    converted to int.

    Args:
        path: Path to the CSV file.

    Returns:
        (X, y) where X is a list of feature lists (floats) and y is a list of
        integer labels.

    Raises:
        ValueError: If any row has fewer than two columns.
    """
    X: List[List[float]] = []
    y: List[int] = []

    with open(path, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                raise ValueError("Each CSV row must have at least two columns")

            values = [float(col) for col in row]
            X.append(values[:-1])
            y.append(int(values[-1]))

    return X, y
