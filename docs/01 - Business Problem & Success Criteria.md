# Business Problem & Success Criteria

A healthcare organization wants a clearer view of how its encounters, costs and payer coverage behave, which procedures drive utilization, which encounter classes drive cost, and how often patients come back.

## Operational Question

> ***Where is encounter volume and cost concentrated, how much of that cost is covered by payers, and which procedures and encounter classes drive utilization?***

Eight sub-questions in the [Analysis Findings](05%20-%20Analysis%20Findings.md) break this down into volume trends, class mix, length of stay, cost by class, payer coverage, procedure frequency, procedure cost and cost by payer.

## Why It Matters

- **Capacity and staffing:** volume trends and class mix show where demand sits.
- **Financial sustainability:** only 30.6% of claim cost is recorded as payer-covered; knowing which payers and classes generate uncovered cost guides revenue-cycle work.
- **Service planning:** a small number of procedures and very expensive encounters drive most of the cost.

## Intended Users and Decisions Supported

**Primary users:** hospital operations managers and the finance / revenue-cycle team.

**Secondary users:** service-line leads (urgent care, ambulatory) and data-governance staff.

**Decisions supported:** where to focus payer-data reconciliation and revenue recovery; whether to introduce insurance-eligibility screening; which service lines and procedures to review for cost and capacity; and which data-quality fixes are needed before these KPIs go into routine reporting.

## Limitations of the Evidence

- The dataset is synthetic and for one hospital, so the results don't generalize to other hospitals.
- Claim cost is billed value, not cash. There are no remittance, denial or claim-status fields, so "zero coverage" can't be told apart from "denied", "pending" or "not recorded".
- No clinical claims or treatment recommendations are made; differences between groups are associations, not causes.
- 2022 is a partial year (to 5 February) and isn't compared with full years.
- There are no admission/discharge or planned-care flags, and return visits are not necessarily readmissions.

## Success Criteria

| Criterion | Measure | Result |
|---|---|---|
| Headline KPIs reconcile | Power BI = Python = SQL; counts exact, currency within $0.01 | Met: 17 of 17 KPIs |
| Totals respond correctly to filters | 4 filter scenarios plus a per-year additivity check | Met: 17 of 17 checks |
| All required analysis covered | 8 questions answered; 5+ KPIs defined; required dashboard pages | Met: 8 questions, 18 KPIs, 6 pages |
| No unnecessary patient identifiers | Names, addresses, ZIP codes and coordinates removed | Met |
| Reproducible | Another analyst can rebuild from the README | Met |
