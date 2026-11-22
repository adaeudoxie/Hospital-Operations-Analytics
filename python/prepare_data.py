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

COPY_AS_IS = ["encounters.csv", "procedures.csv", "payers.csv",
              "organizations.csv", "data_dictionary.csv"]


def main(raw_dir: str) -> None:
    raw = Path(raw_dir).resolve()
    if not (raw / "encounters.csv").exists():
        sys.exit(f"encounters.csv not found in {raw}")
    OUT.mkdir(exist_ok=True)

    for name in COPY_AS_IS:
        shutil.copy2(raw / name, OUT / name)
        print(f"copied   {name}")

    patients = pd.read_csv(raw / "patients.csv", dtype=str)
    dropped = [c for c in patients.columns if c not in PATIENT_KEEP]
    patients[PATIENT_KEEP].to_csv(OUT / "patients_deidentified.csv", index=False)
    print(f"wrote    patients_deidentified.csv  (dropped: {', '.join(dropped)})")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
