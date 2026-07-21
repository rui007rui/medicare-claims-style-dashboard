# Medicare Claims-Style Analytics Dashboard

This project is a public-data portfolio project that uses CMS Medicare Advantage Geographic Variation data to demonstrate a healthcare analytics workflow using Python, SQL, QC checks, GitHub documentation, and a Streamlit dashboard.

The goal is to show not only dashboard development, but also the full analytics process: data review, cleaning, analysis-ready file creation, SQL summaries, quality control, documentation, and delivery.

---

## Live Dashboard Web App

The interactive Streamlit dashboard is deployed here:

https://medicare-ma-dashboard-rui.streamlit.app

---

## Project Purpose

This project demonstrates skills relevant to Medicare claims-style analytics work, including:

- Reading and cleaning CMS public healthcare data
- Handling suppressed values such as `*`
- Creating an analysis-ready dataset
- Writing SQL summary and QC queries
- Building a Streamlit dashboard
- Documenting workflow, business rules, and data definitions
- Using Git and GitHub for version control

---

## Data Source

The project uses CMS public Medicare Advantage Geographic Variation data.

The analysis focuses on selected state-level fields such as:

- Medicare Advantage beneficiary count
- Average beneficiary age
- Dual eligible percentage
- Emergency room visits per 1,000 beneficiaries
- Outpatient visits per 1,000 beneficiaries

Raw source files are not tracked in this GitHub repository. The cleaned analysis-ready file is stored in the `data_processed` folder.

---

## Repository Structure

```text
medicare-claims-style-dashboard/
│
├── dashboard/
│   └── app.py
│
├── data_processed/
│   └── ma_geo_state_2022_analysis.csv
│
├── docs/
│   ├── workflow.md
│   ├── data_dictionary_and_business_rules.md
│   └── qc_report_week1.md
│
├── sql/
│   ├── 01_summary_by_year.sql
│   ├── 02_summary_by_state_latest.sql
│   ├── 03_qc_row_count.sql
│   ├── 04_qc_missing_keys.sql
│   ├── 05_qc_duplicate_state_year.sql
│   ├── 06_qc_beneficiary_count.sql
│   └── 07_qc_missing_utilization.sql
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Dashboard

The Streamlit dashboard is located here:

```text
dashboard/app.py
```

The dashboard includes:

- Year filter
- Medicare Advantage beneficiary KPI
- Average age KPI
- ER visits per 1,000 beneficiaries KPI
- Outpatient visits per 1,000 beneficiaries KPI
- Top 10 states by Medicare Advantage beneficiaries
- Top 10 states by ER visits per 1,000 beneficiaries
- State-level data table
- CSV download option

---

## Documentation

Key project documentation is stored in the `docs` folder:

| Document | Purpose |
|---|---|
| `docs/workflow.md` | Shows the project workflow using a Mermaid diagram |
| `docs/data_dictionary_and_business_rules.md` | Explains key variables, intermediate objects, business rules, and QC logic |
| `docs/qc_report_week1.md` | Summarizes Week 1 data quality checks |

---

## SQL Files

The `sql` folder contains summary and QC queries.

| File | Purpose |
|---|---|
| `01_summary_by_year.sql` | Summarizes data by year |
| `02_summary_by_state_latest.sql` | Summarizes latest-year state-level results |
| `03_qc_row_count.sql` | Checks row counts |
| `04_qc_missing_keys.sql` | Checks missing key fields |
| `05_qc_duplicate_state_year.sql` | Checks duplicate state-year records |
| `06_qc_beneficiary_count.sql` | Checks beneficiary count fields |
| `07_qc_missing_utilization.sql` | Checks missing utilization values |

---

## How to Run the Dashboard

Install required packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run dashboard/app.py
```

---

## Key Cleaning Rule

CMS suppressed values such as `*` are converted to missing values before numeric conversion.

Production-style SQL equivalent:

```sql
TRY_TO_NUMBER(NULLIF(column_name, '*'))
```

Important note:

```text
Suppressed values are not zero. They represent values intentionally not displayed by CMS.
```

---

## Skills Demonstrated

This project demonstrates:

- Python data cleaning
- SQL summary logic
- Healthcare data interpretation
- QC workflow
- Streamlit dashboard development
- GitHub version control
- Technical documentation
- Mermaid workflow documentation
- Portfolio-ready project organization

---

## Project Status

Current status:

```text
Week 1 data cleaning, SQL summaries, QC checks, documentation, and initial Streamlit dashboard completed.
```

Possible next improvements:

- Add dashboard QC section
- Add weighted average calculations
- Add state comparison filters
- Add Streamlit Cloud deployment
- Add screenshots to the repository
- Add additional years of CMS data
```
