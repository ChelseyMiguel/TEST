import matplotlib.pyplot as plt
import pandas as pd


def plot_color_color(df: pd.DataFrame) -> None:
    """Plot WISE color-color diagram with outlier highlighting.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the columns ``w1w2``, ``w2w3``, ``anomaly_score``,
        and ``is_outlier``.
    """
    if not {"w1w2", "w2w3", "is_outlier"}.issubset(df.columns):
        raise ValueError(
            "Input DataFrame must contain 'w1w2', 'w2w3', and 'is_outlier' columns"
        )

    normal = df[df["is_outlier"] == False]
    outliers = df[df["is_outlier"] == True]

    plt.figure(figsize=(8, 6))
    plt.scatter(
        normal["w1w2"],
        normal["w2w3"],
        c="blue",
        label="Normal",
        alpha=0.7,
    )
    plt.scatter(
        outliers["w1w2"],
        outliers["w2w3"],
        c="red",
        marker="*",
        s=150,
        label="Outlier",
    )

    plt.xlabel("W1–W2")
    plt.ylabel("W2–W3")
    plt.title("WISE Color–Color Diagram with IR-Excess Candidates")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("color_color_outliers.png")


if __name__ == "__main__":
    # Example usage with random data
    data = {
        "w1w2": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
        "w2w3": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        "anomaly_score": [0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
        "is_outlier": [False, False, False, True, False, True],
    }
    df_example = pd.DataFrame(data)
    plot_color_color(df_example)
