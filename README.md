# Forex Dashboard

## Overview

Forex Dashboard is a comprehensive tool designed for Forex traders to monitor and analyze their trading performance metrics. By seamlessly integrating with the MT5 terminal on Windows, the tool extracts trading deals, processes the data, and presents it in a user-friendly dashboard using Streamlit. This dashboard provides traders with insights into their daily wins, traded commodities, profit margins, and overall growth percentages.

## Features

- **ETL Process**: Extracts trading data from the MT5 terminal, transforms it for analysis, and loads it into a CSV file.
- **Streamlit Dashboard**: Displays key performance metrics, including:
  - Daily wins and losses.
  - Traded commodities breakdown.
  - Profit gains and losses. 
  - Daily and overall portfolio growth.
  - Commissions paid.
  - Daily and Total Trades executed.
  - Weekly and Monthly gains.

## Prerequisites
- Operating System: Windows (Tested on Windows 11)
- MT5 terminal installed on a Windows machine.
- Python >= 3.11 environment with necessary packages.

## Setup and Usage
1. Create a Conda Environment:

   ```bash
   conda create --name <env_name> python=3.11.6 
   ```

2. Clone the Repository:

   ```bash
   pip install fx_analytics
   pip install MetaTrader5 -> required to access MT5 for your historical trade deals!
   ```

3. To extract all your historical trades data from MT5 Terminal:

   ```python
   import fx_analytics
   from fx_analytics.main_functions import ETL

   
   # replace '****' with your login credential from MT5 terminal!
   mt5_credentials = {'login': '******', 'server':'******','password':'******'}
   df = ETL(from_date='2023-09-01', mt5_credentials = mt5_credentials)
   print(df)
   ```

4. To use/test the streamlit app from the package: To test app you can download the example data 
which was extracted from MT5, download [data](https://github.com/jaybfn/fx_analytics/blob/main/fx_history.csv).
   - Copy the below code into .py file

   ```python
   import fx_analytics 
   from fx_analytics.app import main

   main('fx_history.csv')
   ```

   To Run this file from CLI:
   ```bash
   streamlit run {file_name.py}
   ```

5. To run both ETL to extract your data from MT5 and view the analytics streamlit dashboard
   - create a python script 'app.py' and copy and past the below code, change the 'from_date' with your desired date and 'data_file_path', where you choose to stores the data extracted from ETL function, I prefer to use a data folder eg: 'data/{file_name.csv}'

   ```python
   import fx_analytics 
   from fx_analytics.app import main
   from fx_analytics.main_functions import ETL

   # replace '****' with your login credential from MT5 terminal!
   mt5_credentials = {'login': '******', 'server':'******','password':'******'}
   df = ETL(from_date='2023-09-28', mt5_credentials = mt5_credentials)
   df.to_csv('data_file_path')
   main('data_file_path')
   ```
   To Run this file from CLI:
   ```bash
   streamlit run app.py
   ```

## Output
   - streamlit app preview:
   ![picture alt](https://github.com/jaybfn/fx_analytics/blob/main/fx_analytics/streamlit_preview.jpg?raw=true)

## Feedback and Contribution
- We welcome feedback and contributions! If you encounter any issues or have suggestions, please open an issue. If you'd like to contribute, please create a pull request.
   
   
