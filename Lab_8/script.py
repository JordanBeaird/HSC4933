
#############################################
# Lab 8: Logistic and Poisson Regression     #
# HSC 4933 - Python for Health Analytics     #
#############################################

from pathlib import Path
import re
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from statsmodels.stats.outliers_influence import variance_inflation_factor


def clean_column_names(data):
    """Convert column names to snake_case."""
    data.columns = [
        re.sub(r"[^a-z0-9]+", "_", str(c).strip().lower()).strip("_")
        for c in data.columns
    ]
    return data


def select_predictors(data):
    print("\nAvailable columns:")
    print(", ".join(data.columns))

    predictors = [
        name.strip().lower()
        for name in input(
            "\nEnter predictor columns (separated by commas): "
        ).split(",")
    ]
    response = input("Enter the response column: ").strip().lower()

    if not predictors or any(not name for name in predictors):
        raise ValueError("Enter at least one predictor.")

    if len(predictors) != len(set(predictors)):
        raise ValueError("Do not enter duplicate predictors.")

    if response in predictors:
        raise ValueError("The response cannot also be a predictor.")

    missing = [
        name for name in predictors + [response]
        if name not in data.columns
    ]
    if missing:
        raise ValueError(f"Columns not found: {', '.join(missing)}")

    return predictors, response


def prepare_data(data, predictors, response):
    selected = data[predictors + [response]].copy()

    for column in selected.columns:
        selected[column] = pd.to_numeric(
            selected[column], errors="coerce"
        )

    before = len(selected)
    selected = selected.replace(
        [np.inf, -np.inf], np.nan
    ).dropna()

    print(
        f"\nRows removed for missing/non-numeric values: "
        f"{before - len(selected)}"
    )
    print(f"Rows used: {len(selected)}")

    if selected.empty:
        raise ValueError("No complete numeric rows remain.")

    return selected


def logistic_regression(data, predictors, response):
    y = data[response]

    if not y.isin([0, 1]).all() or y.nunique() != 2:
        raise ValueError(
            "Logistic regression requires a response containing both 0 and 1."
        )

    X = sm.add_constant(
        data[predictors], has_constant="add"
    )
    model = sm.Logit(y, X).fit(disp=False)

    predicted = (model.predict(X) >= 0.5).astype(int)

    output = [
        "LOGISTIC REGRESSION",
        "",
        str(model.summary()),
        "",
        "Note: Classification metrics use training data.",
        f"Accuracy: {accuracy_score(y, predicted):.4f}",
        "",
        "Confusion Matrix (rows = actual; columns = predicted):",
        str(confusion_matrix(y, predicted, labels=[0, 1])),
        "",
        "Classification Report:",
        classification_report(
            y, predicted, labels=[0, 1], zero_division=0
        ),
        f"McFadden Pseudo-R-squared: {model.prsquared:.4f}",
    ]

    return "\n".join(output)


def poisson_regression(data, predictors, response):
    y = data[response]

    if (y < 0).any():
        raise ValueError(
            "Poisson regression requires a nonnegative response."
        )

    warning = ""
    if not np.allclose(y, np.round(y)):
        warning = (
            "WARNING: Response includes fractional values. "
            "Standard Poisson regression assumes integer counts. "
            "Results are exploratory.\n\n"
        )

    X = sm.add_constant(
        data[predictors], has_constant="add"
    )

    model = sm.Poisson(y, X).fit(
        disp=False, maxiter=200
    )

    vif = pd.DataFrame({
        "Predictor": predictors,
        "VIF": [
            variance_inflation_factor(
                X.to_numpy(dtype=float),
                X.columns.get_loc(name)
            )
            for name in predictors
        ]
    })

    return (
        "POISSON REGRESSION\n\n"
        + warning
        + str(model.summary())
        + "\n\nVariance Inflation Factors (VIF):\n"
        + vif.to_string(
            index=False,
            float_format=lambda v: f"{v:.3f}"
        )
        + f"\n\nMcFadden Pseudo-R-squared: {model.prsquared:.4f}"
    )


def main():
    try:
        filename = input(
            "Enter the CSV dataset filename or path: "
        ).strip().strip('"')

        if not Path(filename).is_file():
            raise FileNotFoundError(
                f"File not found: {filename}"
            )

        data = clean_column_names(
            pd.read_csv(filename)
        )

        print(
            f"Loaded {len(data)} rows and "
            f"{len(data.columns)} columns."
        )

        predictors, response = select_predictors(data)

        choice = input(
            "Choose regression (1 = Logistic, 2 = Poisson): "
        ).strip()

        selected = prepare_data(
            data, predictors, response
        )

        if choice == "1":
            result = logistic_regression(
                selected, predictors, response
            )
        elif choice == "2":
            result = poisson_regression(
                selected, predictors, response
            )
        else:
            raise ValueError("Please choose 1 or 2.")

        print("\n" + result)

        save = input(
            "\nSave output to a .txt file? (yes/no): "
        ).strip().lower()

        if save in ("yes", "y"):
            name = input(
                "Enter your output filename: "
            ).strip()

            if not name:
                raise ValueError(
                    "An output filename is required."
                )

            if not name.lower().endswith(".txt"):
                name += ".txt"

            Path(name).write_text(
                result + "\n", encoding="utf-8"
            )

            print(
                f"Saved output to {Path(name).resolve()}"
            )

    except (
        ValueError,
        FileNotFoundError,
        pd.errors.ParserError,
        np.linalg.LinAlgError
    ) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
