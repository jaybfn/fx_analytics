# Forex Dashboard

## Overview

Forex Dashboard is a comprehensive tool designed for Forex traders to monitor and analyze their trading performance metrics. By seamlessly integrating with the MT5 terminal on Windows, the tool extracts trading deals, processes the data, and presents it in a user-friendly dashboard using Streamlit. This dashboard provides traders with insights into their daily wins, traded commodities, profit margins, and overall growth percentages.

## Features

- **ETL Process**: Extracts trading data from the MT5 terminal, transforms it for analysis, and loads it into a CSV file.
- **GitHub Integration**: Pushes the updated CSV to the repository, ensuring data is always up-to-date.
- **Streamlit Dashboard**: Displays key performance metrics, including:
  - Daily wins and losses.
  - Traded commodities breakdown.
  - Profit and loss amounts.
  - Daily and overall growth percentages.
- **Pip Package**: The repository also contains scripts to build a pip package for easy distribution and installation.

## Prerequisites

- MT5 terminal installed on a Windows machine.
- Python==3.11 environment with necessary packages (refer to `requirements.txt` for a detailed list).

## Setup

   **Clone the Repository**:
   ```bash
   pip install fx_analytics

## usage

1. **To extract all your historical trades data from MT5 Terminal**:
   ```bash
   import fx_analytics
   from fx_analytics.main_functions import ETL

   mt5_credentials = {'login': '******', 'server':'******','password':'******'}
   df = ETL(from_date='2023-09-01', mt5_credentials)
   print(df)

2. **To use/test the streamlit app from the package: To test app you can download the example data which was extracted from MT5 from here, click      [data](https://github.com/jaybfn/fx_analytics/blob/main/fx_history.csv)**
   **Copy the below code into .py file**
   ```bash
   import fx_analytics 
   from fx_analytics.app import main

   main('fx_history.csv')

   To Run this file from CLI:
   streamlit run {file_name.py}

3. **To run both ETL to extract your data from MT5 and view the analytics streamlit dashboard**
   - create a python script 'app.py' and copy and past the below code, change the 'from_date' with your desired date and 'data_file_path', where you choose to stores the data extracted from ETL function, I prefer to use a data folder eg: 'data/{file_name.csv}'

   ```bash
   import fx_analytics 
   from fx_analytics.app import main
   from fx_analytics.main_functions import ETL

   mt5_credentials = {'login': '******', 'server':'******','password':'******'}
   df = ETL(from_date='2023-09-28', mt5_credentials)
   df.to_csv('data_file_path')
   main('data_file_path')

   To Run this file from CLI:
   streamlit run app.py

## Feedback and Contribution
- We welcome feedback and contributions! If you encounter any issues or have suggestions, please open an issue. If you'd like to contribute, please create a pull request.
   
   
