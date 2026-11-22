# Executive Summary

**Scope:** 27,891 encounters, 47,701 procedures and 974 patients at Massachusetts General Hospital, January 2011 to 5 February 2022 (synthetic dataset).

**Question:** Where are encounter volume and cost concentrated, how much of that cost do payers cover, and which services drive utilization?

## Headline Indicators

| Indicator | Value | Indicator | Value |
|---|---:|---|---:|
| Total encounters | 27,891 | Payer coverage rate | 30.6% |
| Unique patients | 974 | Encounters with zero payer coverage | 13,586 (48.7%) |
| Total claim cost | $101.5M | Encounters over 24 hours | 75 (0.27%) |
| Avg / median claim cost per encounter | $3,640 / $279 | Procedures performed | 47,701 (163 types) |
| Uncovered claim cost | $70.4M | 30-day return encounters | 16,875 (60.5%) |

## Key Findings

1. **Volume is stable apart from two peaks.** About 2,200–2,500 encounters a year from 2015 to 2020, with peaks in 2014 (3,885) and 2021 (3,530, +40%). The 2021 rise came with more patients (649, the most in any year). 2022 is a partial year.
2. **Care is mostly non-admitted.** Ambulatory (45%), outpatient (23%) and urgent care (13%) make up 81% of encounters; inpatient is 4%.
3. **Cost is concentrated in a few encounters.** The average encounter costs $3,640 but the median is only $279; the top 10% of encounters account for 67% of the $101.5M total.
4. **Urgent care costs far more than its volume suggests:** 13% of encounters but 23% of cost ($23.3M). Electrical cardioversion is the largest procedure cost driver at $35.8M (34% of all procedure cost), and 792 of its 1,383 cases occur in urgent care.
5. **Only 30.6% of claim cost is payer-covered.** Uninsured encounters (31.6% of volume) carry $49.3M, almost half of all claim cost.
6. **Commercial payer data looks incomplete.** Anthem shows zero coverage on all 704 encounters, and Humana, Aetna, Cigna and UnitedHealthcare are above 90% zero-coverage. Blue Cross Blue Shield, by contrast, covers 69%.
7. **Utilization is concentrated.** 60.5% of encounters began within 30 days of the patient's previous one, and the top 10 patients account for 21% of all encounters.
8. **Long stays are rare but poorly recorded.** 0.27% of encounters exceed 24 hours, but 1,077 last exactly 24.0 hours and 13 run for more than 30 days (likely open episodes).

## Recommendations

1. Run a payer-data reconciliation audit for the five commercial payers with near-zero recorded coverage.
2. Introduce insurance-eligibility screening and financial counseling for uninsured patients.
3. Review where high-cost procedures are delivered, starting with cardioversion in urgent care.
4. Fix data capture at the source for discharge times, open episodes and cost reconciliation.
5. Review care coordination for high-utilization patients, separating planned from unplanned returns.

### Recommendation Details

| # | Finding | Action | Intended Benefit | Limitation |
|---:|---|---|---|---|
| 1 | Five commercial payers record near-zero coverage (Anthem 0/704) while BCBS covers 69% | Run a payer-data reconciliation audit to match these payers' encounters to remittance and denial records | Recover unrecorded revenue or correct under-reported coverage; trustworthy coverage KPIs | No claim-status, denial or remittance fields in the dataset |
| 2 | Uninsured encounters make up 31.6% of volume and $49.3M (48.5%) of claim cost; Medicaid covers 94% where it applies | Introduce insurance-eligibility screening and financial counseling at registration | Lower uncovered cost; better access to coverage for patients | No income or eligibility data; share who would qualify is unknown |
| 3 | Urgent care makes up 13% of encounters but 23% of cost; cardioversion takes $35.8M, mostly in urgent care | Review where high-cost procedures are delivered (urgent care vs scheduled outpatient) with clinical leads | Better cost control and capacity planning for the highest-cost service line | No clinical outcome or acuity data; not a clinical recommendation |
| 4 | Duration and cost fields don't reconcile (1,077 stays at exactly 24h; 13 over 30 days; procedure costs above claim in 5,086 encounters) | Fix data capture at the source: record actual discharge times, close open episodes, reconcile line items with claim totals | Reliable length-of-stay and cost KPIs for routine reporting | Needs source-system owners; may change historical figures |
| 5 | Top 10 patients form 21% of encounters; 60.5% of encounters are 30-day returns | Review care coordination for high-utilization patients and separate planned from unplanned returns | Fewer avoidable visits; better capacity forecasting | No planned/unplanned flag; returns ≠ readmissions |
