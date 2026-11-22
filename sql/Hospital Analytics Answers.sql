-- =====================================================================
-- Hospital Operations Analytics: SQL answers (MySQL 8.0+)
-- AnalystLab Africa | Week 3 | Track A
--
-- Answers the questions in hospital_analytics_questions.sql. These
-- queries also act as an independent cross-check of the Power BI
-- dashboard (see docs/06 - Validation Evidence.md).
--
-- Prerequisite: hospital_db created with the provided create_hospital_db.sql.
-- SAFETY: that script starts with DROP DATABASE IF EXISTS hospital_db.
-- Run it ONLY on an isolated practice MySQL instance.
-- =====================================================================
USE hospital_db;

-- ---------------------------------------------------------------------
-- OBJECTIVE 1: ENCOUNTERS OVERVIEW
-- ---------------------------------------------------------------------

-- 1a. Total encounters per year
SELECT YEAR(START) AS encounter_year,
       COUNT(*)    AS total_encounters
FROM encounters
GROUP BY YEAR(START)
ORDER BY encounter_year;

-- 1b. Share of each encounter class within each year (%)
SELECT YEAR(START) AS encounter_year,
       ENCOUNTERCLASS,
       COUNT(*) AS encounters,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY YEAR(START)), 2) AS pct_of_year
FROM encounters
GROUP BY YEAR(START), ENCOUNTERCLASS
ORDER BY encounter_year, pct_of_year DESC;

-- 1c. Encounters over 24 hours vs 24 hours or less
--     "Over" means strictly greater than 24 hours (86,400 seconds).
--     1,077 encounters last exactly 24 hours, so the threshold matters.
SELECT ROUND(100.0 * SUM(TIMESTAMPDIFF(SECOND, START, STOP) >  86400) / COUNT(*), 2) AS pct_over_24h,
       ROUND(100.0 * SUM(TIMESTAMPDIFF(SECOND, START, STOP) <= 86400) / COUNT(*), 2) AS pct_24h_or_less,
       SUM(TIMESTAMPDIFF(SECOND, START, STOP) >  86400) AS n_over_24h,
       SUM(TIMESTAMPDIFF(SECOND, START, STOP) >= 86400) AS n_24h_or_more
FROM encounters;

-- ---------------------------------------------------------------------
-- OBJECTIVE 2: COST & COVERAGE INSIGHTS
-- ---------------------------------------------------------------------

-- 2a. Encounters with zero payer coverage
SELECT SUM(PAYER_COVERAGE = 0) AS zero_coverage_encounters,
       ROUND(100.0 * SUM(PAYER_COVERAGE = 0) / COUNT(*), 2) AS pct_zero_coverage
FROM encounters;

-- 2b. Top 10 most frequent procedures and their average base cost
SELECT DESCRIPTION,
       COUNT(*)                 AS times_performed,
       ROUND(AVG(BASE_COST), 2) AS avg_base_cost
FROM procedures
GROUP BY DESCRIPTION
ORDER BY times_performed DESC
LIMIT 10;

-- 2c. Top 10 procedures by average base cost, with frequency.
--     Version 1, as asked (any frequency):
SELECT DESCRIPTION,
       ROUND(AVG(BASE_COST), 2) AS avg_base_cost,
       COUNT(*)                 AS times_performed
FROM procedures
GROUP BY DESCRIPTION
ORDER BY avg_base_cost DESC
LIMIT 10;

--     Version 2, recommended: only procedures performed at least 10 times,
--     so one-off cases (e.g. ICU admission, n = 5) don't dominate.
SELECT DESCRIPTION,
       ROUND(AVG(BASE_COST), 2) AS avg_base_cost,
       COUNT(*)                 AS times_performed
FROM procedures
GROUP BY DESCRIPTION
HAVING COUNT(*) >= 10
ORDER BY avg_base_cost DESC
LIMIT 10;

-- 2d. Average total claim cost by payer
SELECT p.NAME AS payer,
       COUNT(*) AS encounters,
       ROUND(AVG(e.TOTAL_CLAIM_COST), 2) AS avg_total_claim_cost
FROM encounters e
JOIN payers p ON p.Id = e.PAYER
GROUP BY p.NAME
ORDER BY avg_total_claim_cost DESC;

-- ---------------------------------------------------------------------
-- OBJECTIVE 3: PATIENT BEHAVIOUR ANALYSIS
-- ---------------------------------------------------------------------

-- 3a. Unique patients per quarter
SELECT YEAR(START)    AS yr,
       QUARTER(START) AS qtr,
       COUNT(DISTINCT PATIENT) AS unique_patients
FROM encounters
GROUP BY YEAR(START), QUARTER(START)
ORDER BY yr, qtr;

-- 3b. Patients with a return encounter within 30 days of a previous one.
--     "Previous" = the encounter with the latest earlier START for that patient.
--     Gap = this START minus that encounter's STOP, between 0 and 30 days.
--     NOTE: this is a return visit, not a clinical readmission. Scheduled care
--     (dialysis, hospice, check-ups) is included.
WITH starts AS (
    SELECT PATIENT, START, MAX(STOP) AS max_stop
    FROM encounters
    GROUP BY PATIENT, START
), prev AS (
    SELECT PATIENT, START,
           LAG(max_stop) OVER (PARTITION BY PATIENT ORDER BY START) AS prev_stop
    FROM starts
), flagged AS (
    SELECT e.Id, e.PATIENT,
           TIMESTAMPDIFF(SECOND, p.prev_stop, e.START) / 86400 AS days_since_prev
    FROM encounters e
    JOIN prev p ON p.PATIENT = e.PATIENT AND p.START = e.START
)
SELECT COUNT(*)                AS return_encounters_30d,
       COUNT(DISTINCT PATIENT) AS patients_with_return_30d
FROM flagged
WHERE days_since_prev BETWEEN 0 AND 30;

-- 3c. Patients with the most 30-day return encounters (top 10).
--     Patient Ids only: never output names or addresses.
WITH starts AS (
    SELECT PATIENT, START, MAX(STOP) AS max_stop
    FROM encounters
    GROUP BY PATIENT, START
), prev AS (
    SELECT PATIENT, START,
           LAG(max_stop) OVER (PARTITION BY PATIENT ORDER BY START) AS prev_stop
    FROM starts
)
SELECT e.PATIENT,
       COUNT(*) AS return_encounters_30d
FROM encounters e
JOIN prev p ON p.PATIENT = e.PATIENT AND p.START = e.START
WHERE TIMESTAMPDIFF(SECOND, p.prev_stop, e.START) BETWEEN 0 AND 30 * 86400
GROUP BY e.PATIENT
ORDER BY return_encounters_30d DESC
LIMIT 10;

-- ---------------------------------------------------------------------
-- VALIDATION QUERIES: expected dashboard KPIs (no filters)
-- ---------------------------------------------------------------------
SELECT COUNT(*)                                        AS total_encounters,          -- 27,891
       COUNT(DISTINCT PATIENT)                         AS unique_patients,           -- 974
       ROUND(SUM(TOTAL_CLAIM_COST), 2)                 AS total_claim_cost,          -- 101,514,375.52
       ROUND(AVG(TOTAL_CLAIM_COST), 2)                 AS avg_claim_cost,            -- 3,639.68
       ROUND(SUM(PAYER_COVERAGE), 2)                   AS total_payer_coverage,      -- 31,097,506.99
       ROUND(100 * SUM(PAYER_COVERAGE) / SUM(TOTAL_CLAIM_COST), 2) AS coverage_rate_pct  -- 30.63
FROM encounters;
