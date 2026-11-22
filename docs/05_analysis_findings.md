# Analysis Findings

![Dashboard Overview page](../dashboards/Executive%20Overview.jpg)

*Figure 2. Dashboard Overview page (all six pages are in the `dashboards` folder)*

## Q1. How Have Encounter Volumes Changed Over Time?

| Year | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Encounters | 1,336 | 2,106 | 2,495 | **3,885** | 2,469 | 2,451 | 2,360 | 2,292 | 2,228 | 2,519 | **3,530** | 220 |
| Patients | 410 | 559 | 570 | 630 | 553 | 552 | 546 | 535 | 514 | 519 | 649 | 103 |

*\*2022 runs to 5 Feb only.* Volume peaked in 2014 (+56% on 2013), then held at about 2,200–2,500 a year until 2021 jumped 40%, with unique patients rising too, so the increase reflects more patients rather than heavier use.

**Implication:** plan capacity on the 2015–2020 baseline and confirm the 2021 rise is sustained before treating it as the new normal.

## Q2 & Q4. Encounter Class Share and Claim Cost by Class

| Class | Encounters | Share | Total Claim Cost | Share of Cost | Avg / Encounter | Median / Encounter |
|---|---:|---:|---:|---:|---:|---:|
| Ambulatory | 12,537 | 44.9% | $36.28M | 35.7% | $2,894 | $574 |
| Outpatient | 6,300 | 22.6% | $14.09M | 13.9% | $2,237 | $279 |
| Urgent Care | 3,666 | 13.1% | $23.35M | **23.0%** | $6,369 | $143 |
| Emergency | 2,322 | 8.3% | $10.75M | 10.6% | $4,630 | $146 |
| Wellness | 1,931 | 6.9% | $8.23M | 8.1% | $4,261 | $1,231 |
| Inpatient | 1,135 | 4.1% | $8.81M | 8.7% | **$7,761** | **$2,356** |
| **Total** | **27,891** | **100%** | **$101.51M** | **100%** | **$3,640** | **$279** |

Non-admitted care (ambulatory, outpatient, urgent care) is **80.7%** of encounters, so staffing should follow that mix. Urgent care is the cost outlier; its typical encounter is cheap (median $143), but the top 10% of urgent-care encounters account for 51% of its cost, many involving electrical cardioversion. Inpatient has the highest typical cost. Average cost alone misleads; reviews should target the high-cost tail.

## Q3. What Proportion of Encounters Lasted More Than 24 Hours?

75 encounters (0.27%) lasted more than 24 hours; 58 of them are inpatient, while 1,077 encounters last exactly 24 hours (most inpatient stays).

## Q5 & Q8. Payer Coverage and Claim Cost by Payer

| Payer | Encounters | Avg. Claim | Median Claim | Coverage Rate | Zero-Coverage Share |
|---|---:|---:|---:|---:|---:|
| Medicare | 11,371 | $2,168 | $235 | 78.0% | 0.5% |
| No Insurance | 8,807 | $5,593 | $921 | 0.0% | 100% |
| Medicaid | 1,443 | $6,205 | $1,005 | 94.0% | 0.3% |
| Humana | 1,084 | $3,269 | $279 | 0.1% | 95.8% |
| Aetna | 936 | $2,767 | $279 | 0.1% | 95.9% |
| Blue Cross Blue Shield | 925 | $3,246 | $279 | 69.1% | 36.3% |
| Dual Eligible | 912 | $1,696 | $143 | 89.3% | 13.9% |
| UnitedHealthcare | 900 | $2,848 | $279 | 0.2% | 91.1% |
| Cigna Health | 809 | $2,997 | $279 | 0.04% | 97.7% |
| Anthem | 704 | $4,237 | $279 | 0.0% | 100% |
| **Total** | **27,891** | **$3,640** | **$279** | **30.6%** | **48.7%** |

Payers covered **$31.1M of $101.5M (30.6%)**, leaving $70.4M uncovered, and **13,586 encounters (48.7%)** had zero recorded coverage. Two separate problems are responsible: uninsured care (8,807 encounters carrying 48.5% of all claim cost) and incomplete commercial payer data. Medicaid and uninsured encounters cost the most on average and at the median; commercial payers share the same $279 median, so their averages differ mainly through a few high-cost encounters.

## Q6. Which Procedures Occur Most Frequently?

| # | Procedure | Count | Avg Base Cost |
|---:|---|---:|---:|
| 1 | Assessment of health and social care needs | 4,596 | $431 |
| 2 | Hospice care | 4,098 | $431 |
| 3 | Depression screening using PHQ-2 score | 3,614 | $431 |
| 3 | Depression screening | 3,614 | $431 |
| 5 | Assessment of substance use | 2,906 | $431 |
| 6 | Renal dialysis | 2,746 | $1,004 |
| 7 | Assessment using Morse Fall Scale | 2,422 | $431 |
| 8 | Assessment of anxiety | 2,288 | $431 |
| 9 | Medication reconciliation | 2,284 | $509 |
| 10 | Screening for drug abuse | 1,484 | $431 |

## Q7. Which Procedures Have the Highest Average Base Cost, Considering Frequency?

| Procedure (performed 10+ times) | Count | Avg base cost | Total base cost |
|---|---:|---:|---:|
| Hemodialysis | 27 | $29,300 | $0.79M |
| Electrical cardioversion | 1,383 | $25,903 | $35.82M |
| Percutaneous thrombectomy of portal vein | 57 | $20,228 | $1.15M |
| Surgical manipulation of knee joint | 12 | $16,320 | $0.20M |
| Colonoscopy | 424 | $11,842 | $5.02M |

Without the 10-case minimum, procedures recorded fewer than 10 times dominate (e.g. Admit to ICU, $206,260 from 5 records). Taking frequency into account, electrical cardioversion stands out: both expensive and common, it accounts for **34% of all procedure cost**. Base costs vary widely within a procedure.

## Additional Finding: Return Visits

**16,875 encounters (60.5%)** began within 30 days of the same patient's previous encounter, across 770 of 974 patients (21.5% for wellness to 75.2% for urgent care). The top 10 patients account for **20.6% of all encounters**; one patient has 1,381. This is a return-visit measure, not a clinical readmission rate.
