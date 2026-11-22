"""
Analysis & Validation.py
-----------------------------------------------
Independent recalculation of every KPI and analysis question in the Power BI
dashboard, computed directly from the CSV files with pandas (no Power BI
involved). The results are the "expected values" used in
docs/06 - Validation Evidence.md to check the dashboard.

Usage (from the repository root):
    pip install pandas
    python "python/Analysis & Validation.py"

Outputs (written to outputs/):
    data_quality_profile.csv    column-level profile of every table
    kpi_expected_values.csv     headline KPIs (no filters)
    kpi_filtered_checks.csv     KPIs under filters, to test slicer behaviour
    q1_encounters_by_year.csv   ... one CSV per analysis question (q1-q8)
    return_visits_30d.csv       30-day return-visit summary
"""
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data"
OUT = REPO / "outputs"
OUT.mkdir(exist_ok=True)

CLASS_LABELS = {"ambulatory": "Ambulatory", "outpatient": "Outpatient",
                "urgentcare": "Urgent Care", "emergency": "Emergency",
                "wellness": "Wellness", "inpatient": "Inpatient"}


def load():
    enc = pd.read_csv(DATA / "Encounters.csv")
    proc = pd.read_csv(DATA / "Procedures.csv")
    pay = pd.read_csv(DATA / "Payers.csv")
    pat = pd.read_csv(DATA / "Patients Deidentified.csv")
    org = pd.read_csv(DATA / "Organizations.csv")
    for c in ("START", "STOP"):
        enc[c] = pd.to_datetime(enc[c], utc=True)
        proc[c] = pd.to_datetime(proc[c], utc=True)
    enc["ClassLabel"] = enc["ENCOUNTERCLASS"].map(CLASS_LABELS)
    enc["DurationHours"] = (enc["STOP"] - enc["START"]).dt.total_seconds() / 3600
    enc["Year"] = enc["START"].dt.year
    payer_names = pay.set_index("Id")["NAME"].replace({"NO_INSURANCE": "No Insurance"})
    enc["PayerName"] = enc["PAYER"].map(payer_names)
    return enc, proc, pay, pat, org


def profile(tables):
    rows = []
    for name, df in tables.items():
        for col in df.columns:
            s = df[col]
            rows.append({
                "table": name, "column": col, "dtype": str(s.dtype),
                "rows": len(df), "missing": int(s.isna().sum()),
                "missing_pct": round(s.isna().mean() * 100, 2),
                "distinct": int(s.nunique(dropna=True)),
            })
    return pd.DataFrame(rows)


def add_return_flags(enc):
    """Flag encounters that start within 30 days of the end of the same
    patient's previous encounter. 'Previous' = the encounter with the latest
    START strictly before this one (same definition as the DAX column)."""
    e = enc.copy()
    # For each patient and start time, the latest stop among encounters that
    # began at that time; merge_asof then finds the strictly earlier start.
    starts = (e.groupby(["PATIENT", "START"], as_index=False)["STOP"].max()
                .rename(columns={"START": "PrevStart", "STOP": "PrevStop"}))
    starts = starts.sort_values("PrevStart")
    e = e.sort_values("START")
    e = pd.merge_asof(e, starts, left_on="START", right_on="PrevStart",
                      by="PATIENT", allow_exact_matches=False,
                      direction="backward")
    e["DaysSincePrev"] = (e["START"] - e["PrevStop"]).dt.total_seconds() / 86400
    e["Return30"] = e["DaysSincePrev"].between(0, 30, inclusive="both")
    return e


def main():
    enc, proc, pay, pat, org = load()
    profile({"encounters": enc.iloc[:, :14], "procedures": proc, "payers": pay,
             "patients_deidentified": pat, "organizations": org}
            ).to_csv(OUT / "data_quality_profile.csv", index=False)

    # ---------------- Headline KPIs (no filters) ----------------
    total_claim = enc["TOTAL_CLAIM_COST"].sum()
    total_cov = enc["PAYER_COVERAGE"].sum()
    zero_cov = int((enc["PAYER_COVERAGE"] == 0).sum())
    over24 = int((enc["DurationHours"] > 24).sum())
    ret = add_return_flags(enc)
    kpis = {
        "Total Encounters": len(enc),
        "Unique Patients": enc["PATIENT"].nunique(),
        "Total Claim Cost": round(total_claim, 2),
        "Avg Claim Cost per Encounter": round(total_claim / len(enc), 2),
        "Median Claim Cost": round(enc["TOTAL_CLAIM_COST"].median(), 2),
        "Total Payer Coverage": round(total_cov, 2),
        "Payer Coverage Rate %": round(total_cov / total_claim * 100, 2),
        "Uncovered Cost": round(total_claim - total_cov, 2),
        "Zero Coverage Encounters": zero_cov,
        "Zero Coverage %": round(zero_cov / len(enc) * 100, 2),
        "Encounters Over 24h": over24,
        "% Encounters Over 24h": round(over24 / len(enc) * 100, 2),
        "Total Procedures": len(proc),
        "Avg Procedure Base Cost": round(proc["BASE_COST"].mean(), 2),
        "Total Procedure Base Cost": round(proc["BASE_COST"].sum(), 2),
        "30-Day Return Encounters": int(ret["Return30"].sum()),
        "30-Day Return Rate %": round(ret["Return30"].mean() * 100, 2),
    }
    pd.Series(kpis, name="expected_value").rename_axis("kpi").to_csv(
        OUT / "kpi_expected_values.csv")

    # ---------------- Filtered checks (slicer behaviour) ----------------
    checks = []

    def snap(label, e):
        p = proc[proc["ENCOUNTER"].isin(e["Id"])]
        checks.append({
            "filter": label, "Total Encounters": len(e),
            "Total Claim Cost": round(e["TOTAL_CLAIM_COST"].sum(), 2),
            "Zero Coverage Encounters": int((e["PAYER_COVERAGE"] == 0).sum()),
            "Total Procedures": len(p),
        })

    snap("No filter", enc)
    snap("Year = 2021", enc[enc["Year"] == 2021])
    snap("Encounter Class = Inpatient", enc[enc["ClassLabel"] == "Inpatient"])
    snap("Payer = Medicare", enc[enc["PayerName"] == "Medicare"])
    snap("Year = 2021 AND Class = Emergency",
         enc[(enc["Year"] == 2021) & (enc["ClassLabel"] == "Emergency")])
    by_year_sum = enc.groupby("Year").size().sum()
    checks.append({"filter": "Sum of per-year counts (must equal No filter)",
                   "Total Encounters": int(by_year_sum)})
    pd.DataFrame(checks).to_csv(OUT / "kpi_filtered_checks.csv", index=False)

    # ---------------- Q1: volume over time ----------------
    q1 = enc.groupby("Year").agg(Encounters=("Id", "size"),
                                 UniquePatients=("PATIENT", "nunique"))
    q1["YoY_Change_%"] = (q1["Encounters"].pct_change() * 100).round(1)
    q1.to_csv(OUT / "q1_encounters_by_year.csv")

    # ---------------- Q2: class share ----------------
    q2 = enc.groupby("ClassLabel").size().rename("Encounters").sort_values(ascending=False).to_frame()
    q2["Share_%"] = (q2["Encounters"] / len(enc) * 100).round(2)
    q2.to_csv(OUT / "q2_encounters_by_class.csv")

    # ---------------- Q3: >24h ----------------
    q3 = enc.groupby("ClassLabel").agg(
        Encounters=("Id", "size"),
        Over24h=("DurationHours", lambda s: int((s > 24).sum())),
        MedianHours=("DurationHours", "median"),
        MaxHours=("DurationHours", "max"))
    q3["Over24h_%"] = (q3["Over24h"] / q3["Encounters"] * 100).round(2)
    q3.round(2).to_csv(OUT / "q3_duration_over_24h.csv")

    # ---------------- Q4: claim cost by class ----------------
    q4 = enc.groupby("ClassLabel")["TOTAL_CLAIM_COST"].agg(
        Encounters="size", TotalClaim="sum", AvgClaim="mean",
        MedianClaim="median", MaxClaim="max").sort_values("TotalClaim", ascending=False)
    q4["ShareOfCost_%"] = (q4["TotalClaim"] / total_claim * 100)
    q4.round(2).to_csv(OUT / "q4_claim_cost_by_class.csv")

    # ---------------- Q5: payer coverage ----------------
    q5 = enc.groupby("PayerName").agg(
        Encounters=("Id", "size"),
        TotalClaim=("TOTAL_CLAIM_COST", "sum"),
        TotalCoverage=("PAYER_COVERAGE", "sum"),
        ZeroCoverageEncounters=("PAYER_COVERAGE", lambda s: int((s == 0).sum())))
    q5["CoverageRate_%"] = q5["TotalCoverage"] / q5["TotalClaim"] * 100
    q5["ZeroCoverage_%"] = q5["ZeroCoverageEncounters"] / q5["Encounters"] * 100
    q5.sort_values("Encounters", ascending=False).round(2).to_csv(
        OUT / "q5_payer_coverage.csv")

    # ---------------- Q6/Q7: procedures ----------------
    pg = proc.groupby("DESCRIPTION")["BASE_COST"].agg(
        Count="size", AvgBaseCost="mean", MinBaseCost="min",
        MaxBaseCost="max", TotalBaseCost="sum")
    pg.sort_values("Count", ascending=False).head(10).round(2).to_csv(
        OUT / "q6_top10_procedures_by_frequency.csv")
    pg.sort_values("AvgBaseCost", ascending=False).head(10).round(2).to_csv(
        OUT / "q7a_top10_procedures_by_avg_cost_all.csv")
    pg[pg["Count"] >= 10].sort_values("AvgBaseCost", ascending=False).head(10).round(2).to_csv(
        OUT / "q7b_top10_procedures_by_avg_cost_min10.csv")

    # ---------------- Q8: avg claim by payer ----------------
    q8 = enc.groupby("PayerName")["TOTAL_CLAIM_COST"].agg(
        Encounters="size", AvgClaim="mean", MedianClaim="median"
    ).sort_values("AvgClaim", ascending=False)
    q8.round(2).to_csv(OUT / "q8_avg_claim_by_payer.csv")

    # ---------------- Return visits ----------------
    rv = ret.groupby("ClassLabel").agg(Encounters=("Id", "size"),
                                       Return30=("Return30", "sum"))
    rv["Return30_%"] = (rv["Return30"] / rv["Encounters"] * 100).round(2)
    rv.to_csv(OUT / "return_visits_30d.csv")

    for k, v in kpis.items():
        print(f"{k:32s} {v:>18,}")
    print(f"\nOutputs written to {OUT}")


if __name__ == "__main__":
    main()
