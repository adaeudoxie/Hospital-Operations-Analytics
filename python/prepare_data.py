"""
prepare_data.py
---------------
Copies the AnalystLab Africa Week 3 healthcare dataset into this repository's
`data/` folder and removes patient identifiers that the analysis does not need.

Why: the assignment requires that patient names, addresses and other
unnecessary identifying information are not exposed in reports, dashboards or
public repositories. The raw `patients.csv` holds names, maiden names, street
addresses, ZIP codes and exact coordinates, none of which are needed.

Usage (from the repository root):
    python python/prepare_data.py "<path to the raw Dataset folder>"

Example:
    python python/prepare_data.py "../Dataset"
"""
import shutil
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "data"

# Columns kept from patients.csv. Everything else is a direct or quasi identifier.
PATIENT_KEEP = ["Id", "BIRTHDATE", "DEATHDATE", "MARITAL", "RACE",
                "ETHNICITY", "GENDER", "COUNTY", "STATE"]

# Raw course file name -> name used in this repository's data folder
COPY_AS_IS = {"encounters.csv": "Encounters.csv", "procedures.csv": "Procedures.csv",
              "payers.csv": "Payers.csv", "organizations.csv": "Organizations.csv",
              "data_dictionary.csv": "Data Dictionary.csv"}


def main(raw_dir: str) -> None:
    raw = Path(raw_dir).resolve()
    if not (raw / "encounters.csv").exists():
        sys.exit(f"encounters.csv not found in {raw}")
    OUT.mkdir(exist_ok=True)

    for name, new_name in COPY_AS_IS.items():
        shutil.copy2(raw / name, OUT / new_name)
        print(f"copied   {name} -> {new_name}")

    patients = pd.read_csv(raw / "patients.csv", dtype=str)
    dropped = [c for c in patients.columns if c not in PATIENT_KEEP]
    patients[PATIENT_KEEP].to_csv(OUT / "Patients Deidentified.csv", index=False)
    print(f"wrote    Patients Deidentified.csv  (dropped: {', '.join(dropped)})")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
