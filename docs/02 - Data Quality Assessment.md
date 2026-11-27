# Data Quality Assessment

## Dataset Inventory

Five data files were inspected before modeling. The table shows each file's size, the fields used, and its missing values and data types. No rows are exact duplicates in any file.

| File | Rows × columns | Fields used | Missing values | Types and dates |
|---|---|---|---|---|
| encounters.csv | 27,891 × 14 | Id, START, STOP, PATIENT, PAYER, ENCOUNTERCLASS, BASE_ENCOUNTER_COST, TOTAL_CLAIM_COST, PAYER_COVERAGE | REASONCODE and REASONDESCRIPTION blank in 19,541 rows (70.1%); not used | ISO 8601 UTC timestamps; costs are decimals; codes stored as numbers, typed as text |
| procedures.csv | 47,701 × 9 | ENCOUNTER, PATIENT, START, CODE, DESCRIPTION, BASE_COST | REASONCODE and REASONDESCRIPTION blank in 36,945 rows (77.5%); not used | No primary key; ISO 8601 UTC timestamps; BASE_COST is whole dollars |
| payers.csv | 10 × 7 | Id, NAME | No Insurance row has no address, city, state, ZIP or phone (expected) | Text only |
| organizations.csv | 1 × 8 | Id, NAME | None | One hospital only |
| patients.csv | 974 × 20 | Id, BIRTHDATE, DEATHDATE, MARITAL, RACE, ETHNICITY, GENDER, COUNTY, STATE | DEATHDATE blank for 820 (84%, living patients); MARITAL 1; SUFFIX 953, MAIDEN 588 and ZIP 142 (removed fields) | Dates as yyyy-mm-dd; 11 identifying fields removed before analysis |

The data dictionary uses different capitalization from the CSV headers and lists two patient fields (Middle and FIPS County Code) that are not in patients.csv, so every field used was checked against the CSV itself.

## Issues Found

The dataset is structurally sound. There are no orphan keys across all five relationships, no duplicate IDs or rows, no null or reversed timestamps, no negative costs, and coverage never exceeds claim cost. However, the following issues were discovered:

| Issue | Evidence | Handling |
|---|---|---|
| Partial final year | Data ends 5 Feb 2022 (220 encounters) | Flagged on every page; never compared with full years |
| 24-hour stays | 1,077 stays of exactly 24.0h: ">24h" = 75 vs "≥24h" = 1,152 | Strict definition reported; sensitivity value shown |
| Implausibly long encounters | 13 encounters over 30 days (up to 1,872 days) | Kept; medians used; flagged for source review |
| Highly skewed costs | Median $279 vs mean $3,640; top 10% of encounters = 66.6% of cost | Median shown beside every average |
| Commercial payer coverage | Anthem 0 of 704 covered; four other commercial payers over 90% zero | Reported as "recorded" coverage; completeness risk |
| Cost fields don't reconcile | Procedure costs exceed claim cost in 5,086 encounters; base > total in 89 | Procedure and claim costs never added together |
| Overlapping encounters | 238 encounters start before the previous one ended | Excluded from the 30-day return definition |
