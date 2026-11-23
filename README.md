# Hospital Operations, Cost & Patient Flow Intelligence

**AnalystLab Africa Experience Lab | Week 3 | Track A: Data Analytics**

In this project, I analyzed 27,891 hospital encounters, 47,701 procedures and 974 patients
(January 2011 to February 2022) and built a Power BI dashboard to show where encounter volume
and cost are concentrated, how much of that cost payers cover, and which procedures and
encounter classes drive utilization. I validated every KPI independently in Python and SQL.

![Executive Overview](dashboards/Executive%20Overview.jpg)

## Operational Question

Where is encounter volume and cost concentrated, how much of that cost is covered by payers,
and which procedures and encounter classes drive utilization?

## Headline Results

| KPI | Value |
|---|---:|
| Total encounters | 27,891 |
| Unique patients | 974 |
| Total claim cost | $101.5M |
| Average / median claim cost per encounter | $3,640 / $279 |
| Uncovered claim cost | $70.4M |
| Payer coverage rate | 30.6% |
| Encounters with zero payer coverage | 13,586 (48.7%) |
| Encounters over 24 hours | 75 (0.27%) |
| Procedures performed | 47,701 (163 types) |
| 30-day return encounters | 16,875 (60.5%) |

## Key Findings

- Urgent care makes up 13% of encounters but 23% of claim cost.
- Electrical cardioversion is the largest procedure cost driver at $35.8M (34% of all procedure cost).
- Uninsured encounters carry 48.5% of all claim cost.
- Five commercial payers record near-zero coverage, which points to incomplete payer data.

The full analysis and recommendations are in the [Business Report](docs/Business%20Report.pdf)
and the [Executive Summary](https://github.com/adaeudoxie/Hospital-Operations-Analytics/blob/main/docs/07%20-%20Executive%20Summary.md).

## Dashboard

| | |
|---|---|
| ![Encounter Volume Trends](dashboards/Encounter%20Volume%20Trends.jpg) | ![Encounter Class Comparison](dashboards/Encounter%20Class%20Comparison.jpg) |
| ![Cost & Payer Coverage](dashboards/Cost%20%26%20Payer%20Coverage.jpg) | ![Procedure Utilization](dashboards/Procedure%20Utilization.jpg) |

## Deliverables

| Deliverable | Location |
|---|---|
| Power BI dashboard | `powerbi/HospitalOps.pbix` |
| Dashboard screenshots | `dashboards/` |
| Business report | `docs/Business Report.pdf` |
| Data quality assessment | `docs/02 - Data Quality Assessment.md` |
| KPI definitions | `docs/04 - KPI Definitions.md` and `docs/KPI_Definitions_and_Validation.xlsx` |
| Validation evidence | `docs/06 - Validation Evidence.md` and `powerbi/Validation Query.dax` |
| Executive summary and recommendations | `docs/07 - Executive Summary.md` |

## Approach

The five CSV files (encounters, procedures, payers, patients and organizations) are loaded
into a Power BI star schema, with Encounters at the center and Procedures linked through
Encounter Id. This lets the Year, Encounter Class and Payer slicers filter every visual. The
data model and key transformations are described in
[03 - Data Model & Transformations.md](https://github.com/adaeudoxie/Hospital-Operations-Analytics/blob/main/docs/03%20-%20Data%20Model%20%26%20Transformations.md).

## How to Use This Repository

**Open the dashboard:** open `powerbi/HospitalOps.pbix` in Power BI Desktop. The data is
already loaded. To refresh it from your own copy of the CSVs, go to **Transform data → Edit
parameters**, set **DataFolder** to the full path of the `data` folder (ending with a
backslash), and click **Refresh**.

**Reproduce the validation:**

```bash
pip install pandas
python "python/Analysis & Validation.py"
```

The script recalculates every KPI from the CSVs and saves the results to an `outputs` folder.
To compare them with the dashboard, run `powerbi/Validation Query.dax` in Power BI's DAX query
view and enter the results in `docs/KPI_Definitions_and_Validation.xlsx`.

**SQL:** `sql/Hospital Analytics Answers.sql` answers the reference questions in MySQL 8. It
runs against the database created by the course's `create_hospital_db.sql`. Note that this
script starts by dropping any existing `hospital_db` database, so use a practice MySQL
instance.

**Rebuild the data folder:** the original `patients.csv` contains names, addresses and
coordinates, so it isn't included here. `python/prepare_data.py` recreates the `data` folder
from the original course dataset with those fields removed.

## Limitations

- The dataset is synthetic and for one hospital, so the results don't generalize to other hospitals.
- Claim cost is billed value, not cash. There are no remittance, denial or claim-status fields,
  so "zero coverage" can't be told apart from "denied", "pending" or "not recorded".
- No clinical claims or treatment recommendations are made; differences between groups are
  associations, not causes.
- 2022 is a partial year (to 5 February) and isn't compared with full years.
- Return visits are not necessarily readmissions, as there are no admission/discharge or
  planned-care flags.

## Tools

Power BI Desktop (Power Query, DAX), Python (pandas), SQL (MySQL 8).

The dataset and reference SQL questions come from the AnalystLab Africa Week 3 dataset pack.
