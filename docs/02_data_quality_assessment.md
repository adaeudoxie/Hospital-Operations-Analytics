# Data Quality Assessment

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
