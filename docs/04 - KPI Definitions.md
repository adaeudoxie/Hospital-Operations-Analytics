# KPI Definitions

Values are for the full dataset with no filters.

| KPI | Definition | Value |
|---|---|---:|
| Total encounters | Number of encounter records | 27,891 |
| Unique patients | Distinct patients with at least one encounter | 974 |
| Total claim cost | Sum of TOTAL_CLAIM_COST (billed value, not cash) | $101,514,375.52 |
| Avg / median claim cost | Total claim cost ÷ encounters; middle encounter value | $3,639.68 / $278.58 |
| Total payer coverage | Sum of PAYER_COVERAGE | $31,097,506.99 |
| Payer coverage rate | Payer coverage ÷ total claim cost (cost-weighted) | 30.63% |
| Uncovered cost | Total claim cost − payer coverage | $70,416,868.53 |
| Zero-coverage encounters / % | Encounters where PAYER_COVERAGE = 0 | 13,586 / 48.71% |
| Encounters over 24h / % | Stop − Start strictly greater than 24 hours | 75 / 0.27% |
| Encounters 24h or more | Sensitivity check including exactly-24h stays | 1,152 |
| Total procedures / avg base cost | Procedure records; mean BASE_COST per procedure | 47,701 / $2,212.06 |
| Avg base cost (10+ procedures) | Average base cost shown only where performed at least 10 times | Varies |
| 30-day return encounters / rate | Encounter starting 0–30 days after the end of the same patient's previous one | 16,875 / 60.50% |

## DAX Formulas

These are the DAX measures used in the Power BI model for each KPI above.

| KPI | DAX |
|---|---|
| Total encounters | `COUNTROWS ( Encounters )` |
| Unique patients | `DISTINCTCOUNT ( Encounters[Patient Id] )` |
| Total claim cost | `SUM ( Encounters[Claim Cost] )` |
| Avg claim cost | `DIVIDE ( [Total Claim Cost], [Total Encounters] )` |
| Median claim cost | `MEDIAN ( Encounters[Claim Cost] )` |
| Total payer coverage | `SUM ( Encounters[Coverage Amount] )` |
| Payer coverage rate | `DIVIDE ( [Total Payer Coverage], [Total Claim Cost] )` |
| Uncovered cost | `[Total Claim Cost] - [Total Payer Coverage]` |
| Zero-coverage encounters | `CALCULATE ( [Total Encounters], Encounters[Zero Coverage] = TRUE () ) + 0` |
| Zero-coverage % | `DIVIDE ( [Zero Coverage Encounters], [Total Encounters] )` |
| Encounters over 24h | `CALCULATE ( [Total Encounters], Encounters[Over 24 Hours] = TRUE () ) + 0` |
| % encounters over 24h | `DIVIDE ( [Encounters Over 24h], [Total Encounters] )` |
| Encounters 24h or more | `CALCULATE ( [Total Encounters], Encounters[Duration Hours] >= 24 ) + 0` |
| Total procedures | `COUNTROWS ( Procedures )` |
| Avg procedure base cost | `AVERAGE ( Procedures[Base Cost] )` |
| Avg base cost (10+ procedures) | `IF ( [Total Procedures] >= 10, [Avg Procedure Base Cost] )` |
| 30-day return encounters | `CALCULATE ( [Total Encounters], Encounters[Return Within 30 Days] = TRUE () ) + 0` |
| 30-day return rate | `DIVIDE ( [30-Day Return Encounters], [Total Encounters] )` |
