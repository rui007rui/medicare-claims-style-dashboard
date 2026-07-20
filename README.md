# Medicare Claims-Style Analytics Dashboard

## Project Purpose

This project uses public CMS Medicare Advantage Geographic Variation data to demonstrate a Medicare claims-style analytics workflow using Python, SQL-style summaries, Streamlit dashboard reporting, and data quality checks.

The goal is to rebuild and demonstrate current healthcare data programming skills, including data cleaning, summary analysis, dashboard development, and claims-style QC thinking.

## Data Source

Dataset: CMS Medicare Advantage Geographic Variation - National & State, 2022

The dataset includes Medicare Advantage enrollment, beneficiary demographics, dual eligibility percentage, and utilization measures by year and state.

## Tools Used

- Python
- pandas
- DuckDB / SQL-style queries
- Streamlit
- Matplotlib
- Google Colab
- GitHub

## Project Structure

medicare-claims-style-dashboard/
- README.md
- dashboard/app.py
- data_processed/ma_geo_state_2022_analysis.csv
- sql/
- docs/
- screenshots/

## Current Dashboard Features

- Year filter
- KPI cards
- Medicare Advantage beneficiary count
- Average beneficiary age
- ER visits per 1,000 beneficiaries
- Outpatient visits per 1,000 beneficiaries
- Top 10 states by Medicare Advantage enrollment
- Top 10 states by ER utilization
- State-level data table
- CSV download button

## Data Cleaning and QC

Key cleaning steps:

- Identified CMS suppressed values marked as *
- Converted suppressed values to missing values
- Selected dashboard analysis fields
- Converted numeric fields
- Created analysis-ready CSV

Planned QC checks:

- Row count validation
- Missing value check
- Duplicate state-year check
- Negative or zero beneficiary count check
- Utilization measure missingness check

## Interview Summary

I built this project to demonstrate my current Python, SQL, dashboard, and QC skills using public CMS Medicare Advantage data. The workflow reflects the type of Medicare/Medicaid data work I have done in claims projects: understand the data, clean it, validate it, summarize it, and deliver results clearly.
