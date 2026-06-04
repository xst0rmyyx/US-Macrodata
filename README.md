# Economic-Data

A lightweight Python toolkit for downloading, storing, and building clean datasets from the [Federal Reserve Bank of St. Louis’ FRED API](https://fred.stlouisfed.org/). Designed for economists, analysts, and researchers who want a simple, reproducible way to work with macroeconomic time series data.

-----

## Features

- Download any FRED time series by its Series ID
- Automatically store data in a local SQLite database (`Fred.db`) to avoid redundant API calls
- Build clean, analysis-ready CSV datasets with configurable data wrangling options
- Works fully offline once data has been downloaded

-----

## Project Structure

```
Economic-Data/
├── fred/
│   ├── database.py       # FredDatabase class – handles API calls & local DB storage
│   ├── schema.py         # Pydantic schema for fred/configs.json
│   └── configs.json      # Your FRED API key (created by you)
├── data/
│   ├── wrangling.py      # Dataset building logic
│   ├── schema.py         # Pydantic schema for data/configs.json
│   └── configs.json      # Data wrangling configuration
├── utils/
│   └── validation.py     # JSON config validation helpers
├── download.py           # Script to download & store FRED series
└── dataset.py            # Script to build a clean CSV dataset
```

-----

## Requirements

- Python 3.10+
- [fredapi](https://github.com/mortada/fredapi)
- pandas
- pydantic
- sqlite3 *(part of Python’s standard library)*
- logging, pathlib, json, typing, time, re *(part of Python’s standard library)*

Install the third-party dependencies with:

```bash
pip install fredapi pandas pydantic
```

-----

## Setup

### 1. Get a FRED API Key

Create a free account at [fred.stlouisfed.org](https://fred.stlouisfed.org/) and request an API key under your account settings.

### 2. Configure your API Key

Create the file `fred/configs.json` and add your key:

```json
{
    "api_key": "YOUR_API_KEY_HERE"
}
```

### 3. Configure Data Wrangling (optional)

The file `data/configs.json` controls how raw data is cleaned and transformed when building a dataset. A default configuration is shown below – you can adjust it to your needs:

```json
{
    "startdate": "2000-01-01",
    "enddate": "null",
    "resample_period": "Q",
    "row_threshold": 0.30,
    "col_threshold": 0.20,
    "interpolate_fill": [
        "PAYEMS",
        "CPIAUCSL",
        "CPILFESL",
        "PCEPI",
        "PCEPILFE",
        "GDPC1",
        "RSXFS",
        "WALCL",
        "GDP"
    ],
    "mean_fill": [
        "UNRATE",
        "ICSA",
        "JTSJOL",
        "INDPRO",
        "FEDFUNDS",
        "T10Y2Y",
        "T10YIE",
        "DGS10"
    ]
}
```

For a description of each field, refer to `data/schema.py`.

-----

## Usage

The two main scripts can be used **independently** of each other.

### Download Data

`download.py` fetches one or more FRED series and saves them to the local database (`Fred.db`). Use this if you just want to build up a local cache of raw data.

```bash
python download.py
```

You can edit the script to specify which Series IDs and at what frequency to download.

-----

### Build a Dataset

`dataset.py` fetches series data (from the local database if available, otherwise via the API), applies the wrangling steps defined in `data/configs.json`, and exports a clean CSV file.

```python
from dataset import main

main(
    series_ids=['GDPC1', 'RSXFS', 'INDPRO', 'PCEPILFE'],
    frequency='q',
    target_path='my_dataset.csv'
)
```

Or run it directly with the default settings:

```bash
python dataset.py
```

**Parameters:**

|Parameter    |Type       |Default        |Description                                                                                 |
|-------------|-----------|---------------|--------------------------------------------------------------------------------------------|
|`series_ids` |`list[str]`|See script     |FRED Series IDs to include                                                                  |
|`frequency`  |`str`      |`'q'`          |Frequency: `'d'` (daily), `'w'` (weekly), `'m'` (monthly), `'q'` (quarterly), `'a'` (annual)|
|`target_path`|`str`      |`'dataset.csv'`|Output path for the CSV file (must end in `.csv`)                                           |


> **How it works:** `dataset.py` checks the local `Fred.db` database first. If the requested series is already stored locally, it loads it from there. If not, it fetches the data from the FRED API and saves it to the database for future use (as long as `autosave=True`).

-----

## Example Series IDs

Not sure where to start? Here are some commonly used FRED series:

|Series ID |Description                               |
|----------|------------------------------------------|
|`GDPC1`   |Real GDP (Quarterly)                      |
|`UNRATE`  |Unemployment Rate                         |
|`CPIAUCSL`|Consumer Price Index (All Urban Consumers)|
|`FEDFUNDS`|Federal Funds Effective Rate              |
|`INDPRO`  |Industrial Production Index               |
|`DGS10`   |10-Year Treasury Constant Maturity Rate   |

You can browse all available series at [fred.stlouisfed.org](https://fred.stlouisfed.org/).

-----

## License

This project is licensed under the [MIT License](LICENSE).
