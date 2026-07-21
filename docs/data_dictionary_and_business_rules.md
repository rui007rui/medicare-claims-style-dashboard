# Data Dictionary and Business Rules

This document explains the key source variables, intermediate datasets, dashboard output logic, and QC checks used in this Medicare Advantage public-data dashboard project.

The purpose is not to document every column in the raw CMS file. Instead, this document focuses on the important fields and logic used in the analysis, dashboard, and quality control workflow.

---

## 1. Key Source Variables Used

These variables come from the CMS public Medicare Advantage Geographic Variation data.

| Variable | Meaning | Type | Use in Project | Notes |
|---|---|---|---|---|
| YEAR | Calendar year of the data record | Numeric | Used for dashboard year filter | The dashboard defaults to the latest available year |
| STATE | State abbreviation or national row | Text | Used for state-level summaries and charts | National row may need special handling depending on analysis |
| BENE_GEO_CD | Beneficiary geographic code | Numeric | Geographic identifier | Used as supporting geographic field |
| BENES_MA_CNT | Number of Medicare Advantage beneficiaries | Numeric | Used for enrollment KPI and top 10 state chart | Larger states usually have higher counts |
| BENE_AVG_AGE | Average beneficiary age | Numeric | Used as population characteristic | Helps describe state MA population |
| BENE_FEML_PCT | Percent of beneficiaries who are female | Numeric percentage | Used as demographic field | Original CMS field |
| BENE_MALE_PCT | Percent of beneficiaries who are male | Numeric percentage | Used as demographic field | Original CMS field |
| BENE_DUAL_PCT | Percent of beneficiaries who are dual eligible for Medicare and Medicaid | Numeric percentage | Used as population complexity measure | Some values may be suppressed by CMS |
| BENES_OP_CNT | Number of beneficiaries with outpatient services | Numeric | Used as outpatient utilization count | Original CMS field |
| BENES_OP_PCT | Percent of beneficiaries with outpatient services | Numeric percentage | Used as outpatient utilization measure | Original CMS field |
| OP_VISITS_PER_1000_BENES | Outpatient visits per 1,000 beneficiaries | Numeric rate | Used in dashboard table and comparison | Rate allows comparison across states |
| BENES_ER_VISITS_CNT | Number of beneficiaries with ER visits | Numeric | Used as ER utilization count | Original CMS field |
| BENES_ER_VISITS_PCT | Percent of beneficiaries with ER visits | Numeric percentage | Used as ER utilization measure | Original CMS field |
| ER_VISITS_PER_1000_BENES | ER visits per 1,000 beneficiaries | Numeric rate | Used for top 10 ER visit chart | Rate allows comparison across states |

---

## 2. Cleaning Rules

### Suppressed CMS Values

CMS uses `*` to indicate suppressed values. Suppression is commonly used to protect privacy or avoid displaying small-cell values.

Project cleaning rule:

```text
If value = "*", convert to missing value / NaN.
```

Important note:

```text
Suppressed value is not zero.
Suppressed value is not the same as a confirmed missing source value.
Suppressed value means CMS intentionally did not display the value.
```

### Numeric Conversion

Several fields were read as text because of suppressed values or formatting. After replacing `*` with missing values, selected fields were converted to numeric type.

Project cleaning rule:

```text
Convert selected analysis fields to numeric using safe conversion logic.
Values that cannot be converted become missing.
```

Production-style SQL equivalent:

```sql
TRY_TO_NUMBER(NULLIF(column_name, '*'))
```

### Row Retention

Rows were not deleted during the main cleaning step.

Project rule:

```text
Keep all rows.
Replace suppressed cell values with missing values.
Convert selected fields to numeric.
```

---

## 3. Important Intermediate Datasets / Objects

These objects are used inside the Python and dashboard workflow.

| Object | Type | Meaning | Use | Business / QC Note |
|---|---|---|---|---|
| df | Raw loaded dataset | CMS CSV loaded into Python | Starting point for cleaning | Should match raw CMS row count |
| df_clean | Intermediate dataset | Dataset after suppressed `*` values are converted to missing | Used before selecting analysis fields | Row count should remain unchanged |
| analysis_cols | Column list | Selected fields used for analysis and dashboard | Defines project scope | Helps avoid carrying unnecessary raw columns |
| numeric_cols | Column list | Fields converted from text to numeric | Supports analysis and charting | Important for avoiding text-based calculation errors |
| df_analysis | Analysis dataset | Cleaned and selected dataset used for project outputs | Saved as analysis-ready CSV | Main dataset for SQL and dashboard |
| df_year | Dashboard filtered dataset | Records filtered to selected dashboard year | Used for KPI cards, charts, and tables | Should contain the expected state-level records for that year |
| top10_benes | Dashboard output dataset | Top 10 states by MA beneficiary count | Used for enrollment bar chart and table | Sorted by `BENES_MA_CNT` descending |
| top10_er | Dashboard output dataset | Top 10 states by ER visits per 1,000 beneficiaries | Used for ER utilization bar chart and table | Sorted by `ER_VISITS_PER_1000_BENES` descending |

---

## 4. Dashboard Business Rules

### Year Filter

Rule:

```text
The dashboard allows the user to select a year from available YEAR values.
The default selected year is the latest available year.
```

Use:

```text
All KPI cards, charts, and tables are based on the selected year.
```

### Medicare Advantage Beneficiary KPI

Rule:

```text
Sum BENES_MA_CNT for the selected year.
```

Use:

```text
Shows overall Medicare Advantage beneficiary count for the selected dashboard view.
```

Caution:

```text
If national and state records are both included, totals may be double-counted.
National rows should be reviewed and handled carefully depending on the intended analysis.
```

### Average Age KPI

Rule:

```text
Calculate the mean of BENE_AVG_AGE for the selected year.
```

Use:

```text
Shows average age across selected records.
```

Caution:

```text
Simple average across states is not the same as beneficiary-weighted average.
For production analysis, a weighted average may be more appropriate.
```

### ER Visits per 1,000 KPI

Rule:

```text
Calculate the mean of ER_VISITS_PER_1000_BENES for the selected year.
```

Use:

```text
Shows a high-level ER utilization measure.
```

Caution:

```text
Simple average across states is not the same as beneficiary-weighted rate.
```

### Outpatient Visits per 1,000 KPI

Rule:

```text
Calculate the mean of OP_VISITS_PER_1000_BENES for the selected year.
```

Use:

```text
Shows a high-level outpatient utilization measure.
```

Caution:

```text
Simple average across states is not the same as beneficiary-weighted rate.
```

### Top 10 States by MA Beneficiaries

Rule:

```text
Filter data to selected year.
Sort by BENES_MA_CNT descending.
Keep first 10 rows.
```

Use:

```text
Shows states with the largest MA enrollment counts.
```

### Top 10 States by ER Visits per 1,000 Beneficiaries

Rule:

```text
Filter data to selected year.
Sort by ER_VISITS_PER_1000_BENES descending.
Keep first 10 rows.
```

Use:

```text
Shows states with the highest ER visit rates among MA beneficiaries.
```

---

## 5. QC Checks

QC checks are used to make sure the analysis-ready data and dashboard outputs are reasonable.

| QC Check | Purpose | Expected Result | Why It Matters |
|---|---|---|---|
| Row count check | Confirms row counts before and after cleaning | Row count should remain stable during suppression replacement | Prevents accidental row deletion |
| Missing key check | Checks whether key fields such as YEAR or STATE are missing | Key fields should not be missing | Missing keys can break grouping, filtering, and joins |
| Duplicate state-year check | Checks whether the same STATE and YEAR appears more than expected | No unexpected duplicates | Duplicates can overcount beneficiaries and distort charts |
| Beneficiary count check | Checks whether beneficiary counts are valid and reasonable | Counts should be non-missing and non-negative where expected | Invalid counts affect enrollment summaries |
| Missing utilization check | Checks missing values in ER and outpatient utilization fields | Missing values should be understood and explained | Missing rates affect rankings and dashboard interpretation |
| Suppressed value check | Confirms that `*` values were converted to missing values | No remaining `*` in analysis dataset | Prevents numeric conversion and calculation problems |

---

## 6. Derived Variables

At this stage, the project mainly uses original CMS fields after cleaning and type conversion.

No major new derived analytic variables have been created yet.

Future derived variables may include:

| Derived Variable | Possible Meaning | Possible Rule |
|---|---|---|
| high_er_flag | Indicates states with high ER utilization | Flag states above a selected ER visit threshold |
| high_dual_flag | Indicates states with high dual eligible percentage | Flag states above a selected dual percentage threshold |
| weighted_avg_age | Beneficiary-weighted average age | Sum age weighted by beneficiary count |
| utilization_category | Groups states into low, medium, high utilization | Based on percentile or fixed threshold |

---

## 7. Documentation Principle

This project does not attempt to document every raw CMS variable.

The documentation focuses on:

```text
Important final output variables
Important intermediate variables
Important business rules
Important QC checks
Fields that may be misunderstood
```

This approach is closer to real healthcare analytics work, where documentation should explain the logic that affects results, review, QC, and delivery.
```
