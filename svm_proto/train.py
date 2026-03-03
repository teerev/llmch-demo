import argparse
import json

from svm_proto.data import load_csv
from svm_proto.svm import LinearSVM


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a LinearSVM model from CSV data.")
    parser.add_argument("--data", required=True, help="Path to input CSV data")
    parser.add_argument("--model-out", required=True, help="Path to output JSON model file")
    parser.add_argument("--epochs", type=int, default=1000, help="Number of training epochs")
    parser.add_argument("--lr", type=float, default=0.01, help="Learning rate")
    parser.add_argument("--C", type=float, default=1.0, help="Regularization strength")

    args = parser.parse_args()

    X, y = load_csv(args.data)
    model = LinearSVM(learning_rate=args.lr, epochs=args.epochs, C=args.C)
    model.fit(X, y)

    with open(args.model_out, "w", encoding="utf-8") as f:
        json.dump(model.to_dict(), f)


if __name__ == "__main__":
    main()
