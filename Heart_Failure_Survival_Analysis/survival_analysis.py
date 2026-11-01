"""Heart Failure Survival Analysis

Purpose: Compare time to readmission using Kaplan-Meier/log-rank methods,
and model time to death using Cox proportional hazards regression.
Data: Course-provided CSV files; no patient records are embedded in this script.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import logrank_test, proportional_hazard_test


DATA_DIR = Path(__file__).resolve().parent


def analyze_readmission():
    """Plot Kaplan-Meier curves and test treatment-group differences."""
    data = pd.read_csv(DATA_DIR / "km_logrank_readmission.csv")
    standard = data.loc[data["treatment_group"] == "Standard care"]
    telehealth = data.loc[data["treatment_group"] == "Telehealth follow-up"]

    if standard.empty or telehealth.empty:
        raise ValueError("Expected Standard care and Telehealth follow-up groups.")

    result = logrank_test(
        standard["time_days"],
        telehealth["time_days"],
        event_observed_A=standard["readmitted"],
        event_observed_B=telehealth["readmitted"],
    )

    fig, ax = plt.subplots(figsize=(9, 6))
    km = KaplanMeierFitter()
    for label, group in [("Standard care", standard), ("Telehealth follow-up", telehealth)]:
        km.fit(group["time_days"], event_observed=group["readmitted"], label=label)
        km.plot_survival_function(ax=ax, ci_show=True)

    ax.set(title="Time to Hospital Readmission by Treatment Group",
           xlabel="Days after discharge", ylabel="Probability of remaining readmission-free",
           xlim=(0, 180), ylim=(0, 1.02))
    ax.text(0.03, 0.05, f"Log-rank statistic = {result.test_statistic:.2f}\np-value = {result.p_value:.3g}",
            transform=ax.transAxes, bbox={"facecolor": "white", "alpha": 0.9})
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(DATA_DIR / "kaplan_meier_logrank.png", dpi=200)
    print("\nLOG-RANK TEST")
    print(result.summary.to_string())
    return fig


def analyze_mortality():
    """Fit a Cox model and plot covariate hazard ratios with 95% CIs."""
    data = pd.read_csv(DATA_DIR / "cox_ph_heart_failure_survival.csv")
    # Patient IDs are identifiers, not predictors. Encode male sex as 1.
    model_data = data.drop(columns=["patient_id"]).copy()
    model_data["sex"] = model_data["sex"].map({"Female": 0, "Male": 1})
    if model_data.isna().any().any():
        raise ValueError("Unexpected missing or unrecognized values in model data.")

    model = CoxPHFitter()
    model.fit(model_data, duration_col="time_months", event_col="death")
    print("\nCOX PROPORTIONAL HAZARDS MODEL")
    print(model.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%", "p"]].to_string())

    # Schoenfeld residual test provides a diagnostic of the PH assumption.
    ph_result = proportional_hazard_test(model, model_data, time_transform="rank")
    print("\nPROPORTIONAL HAZARDS ASSUMPTION CHECK")
    print(ph_result.summary.to_string())

    summary = model.summary.sort_values("exp(coef)")
    y = np.arange(len(summary))
    hazard_ratios = summary["exp(coef)"].to_numpy()
    lower = summary["exp(coef) lower 95%"].to_numpy()
    upper = summary["exp(coef) upper 95%"].to_numpy()

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.errorbar(hazard_ratios, y,
                xerr=[hazard_ratios - lower, upper - hazard_ratios],
                fmt="o", capsize=3)
    ax.axvline(1, color="gray", linestyle="--", label="No effect (HR = 1)")
    ax.set_yticks(y, summary.index)
    ax.set_xscale("log")
    ax.set(title="Cox Model: All-Cause Mortality Hazard Ratios",
           xlabel="Hazard ratio (log scale) with 95% confidence interval")
    ax.grid(axis="x", alpha=0.2)
    ax.legend()
    fig.tight_layout()
    fig.savefig(DATA_DIR / "cox_proportional_hazards.png", dpi=200)
    return fig


def main():
    analyze_readmission()
    analyze_mortality()
    print("\nSaved both figures to:", DATA_DIR)
    plt.show()


if __name__ == "__main__":
    main()
