# Architecture

## Stage 1
- Generate synthetic raw tables.
- Persist CSV in bronze and exports/csv.
- Persist JSON and SQLite for portability.
- Keep silver and gold empty until ETL.

## Stage 2
- Validate schema and business rules.
- Build cleaned silver tables.

## Stage 3
- Build analytical gold marts.
