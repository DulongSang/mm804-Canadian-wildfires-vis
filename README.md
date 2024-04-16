# MM804 Winter2024 Final Project

## Group Members
- Dulong Sang: dulong
- Swati Chowdhury: schowdh4
- Bala Srujan Kumar Reddy Gade: balasruj

## Dependencies
- Python >= 3.9
- dash >= 2.16
- pandas >= 2.10

### Install Pypi Dependencies
```bash
pip install dash
pip install pandas
```

## Instruction to Run
Before running the app, please download data from CWFIS using the following commands.

### Download dataset from CWFIS
```bash
python3 scripts/download_cwfis.py '2024-01-01' '2024-03-01' ./hotspots
```

### Combine daily csv files
```bash
python3 scripts/combine_csv.py ./hotspots ./hotspots.csv
```

### Run the App
```bash
python3 src/app.py -f ./hotspots.csv [--port=24804] [--debug]
```
