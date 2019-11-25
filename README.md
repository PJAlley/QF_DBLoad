# QF Data Loading

This is a take-home to load data into a DB and to calculate the classification totals.

It will create two tables called DELoad and classification_totals into a local SQLite database which is stored locally.

The script will also delete those tables if they already exist, ensuring a clean slate.

## Usage
```
python3 load_data.py
```

## Tables

### DELoad

This table simply loads the data from a CSV file called `DataEngineerDataSet.csv`. The criteria to load is: if the first column contains three numbers separated by two dots, it is loaded.

### classification_totals

This table is the count of classifications from DELoad. Only classifications that are not blank and ones not labled `(not assigned)` are counted.
