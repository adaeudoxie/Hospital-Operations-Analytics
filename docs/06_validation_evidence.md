# Validation

Every KPI was calculated three independent ways:

1. the Power BI model (DAX query view on the refreshed dashboard),
2. a Python script reading the CSVs directly, and
3. SQL queries.

All three agree exactly: counts to the unit, currency to the cent.

| KPI | Power BI | Python | SQL |
|---|---:|---:|---:|
| Total encounters | 27,891 | 27,891 | 27,891 |
| Unique patients | 974 | 974 | 974 |
| Total claim cost | $101,514,375.52 | $101,514,375.52 | $101,514,375.52 |
| Total payer coverage | $31,097,506.99 | $31,097,506.99 | $31,097,506.99 |
| Zero-coverage encounters | 13,586 | 13,586 | 13,586 |
| Encounters over 24h / 24h or more | 75 / 1,152 | 75 / 1,152 | 75 / 1,152 |
| 30-day return encounters | 16,875 | 16,875 | 16,875 |

**Filter checks:** four filter scenarios (Year = 2021; Class = Inpatient; Payer = Medicare; 2021 + Emergency) were checked for encounters, claim cost, zero-coverage and procedure counts, and all 16 values matched. The yearly encounter counts add up to the 27,891 total.
