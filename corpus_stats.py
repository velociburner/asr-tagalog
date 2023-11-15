from collections import Counter
from pathlib import Path


def count_tokens(dir: Path):
    counts: Counter[str] = Counter()
    for path in dir.glob("*.txt"):
        with path.open('r', encoding='utf8') as f:
            for line in f:
                counts.update(line.strip().split())
    return counts


def main(train: Path, dev: Path, test: Path):
    train_counts = count_tokens(train)
    dev_counts = count_tokens(dev)
    test_counts = count_tokens(test)

    print("Train split:")
    print(f"\tTypes: {len(train_counts)}")
    print(f"\tTokens: {sum(train_counts.values())}")

    print("Dev split:")
    print(f"\tTypes: {len(dev_counts)}")
    print(f"\tTokens: {sum(dev_counts.values())}")

    print("Test split:")
    print(f"\tTypes: {len(test_counts)}")
    print(f"\tTokens: {sum(test_counts.values())}")

    print()
    print(f"{len(dev_counts - train_counts)} OOV types in Dev")
    print(f"{len(test_counts - train_counts)} OOV types in Test")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--train",
        type=Path,
        default=Path("train"),
        help="Directory for train partition containing .txt files"
    )
    parser.add_argument(
        "--dev",
        type=Path,
        default=Path("dev"),
        help="Directory for dev partition containing .txt files"
    )
    parser.add_argument(
        "--test",
        type=Path,
        default=Path("test"),
        help="Directory for test partition containing .txt files"
    )
    args = parser.parse_args()

    main(args.train, args.dev, args.test)
