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
- Python environment with necessary packages (refer to `requirements.txt` for a detailed list).
- GitHub account for data synchronization.

## Setup and Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jaybfn/fx_analytics.git
   cd fx_analytics

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Run the ETL script**:
   ```bash
   python ETL.py

4. **Launch the streamlit Bashboard**:
   ```bash
   streamlit run app.py

5. **If you want to run ETL.py and app.py together then**:
   - I have commented git commands as this file also updates all the changes to the git once the file is run (it could be usefull if you deploy you   streamlit app to the server)
   ```bash
   python main_run.py

## Feedback and Contribution
- We welcome feedback and contributions! If you encounter any issues or have suggestions, please open an issue. If you'd like to contribute, please create a pull request.
   
   
