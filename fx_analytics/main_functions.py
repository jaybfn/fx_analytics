import os
import MetaTrader5 as mt5
from datetime import datetime, date
from typing import List, Dict
import pandas as pd
from loguru import logger
import plotly.express as px
import plotly.graph_objects as go
from fx_analytics import config


def setup_logging(log_file):
    """
    Set up logging to a file.

    Args:
        log_file (str): The path to the log file.

    Returns:
        None
    """
    logger.remove()  # Remove any previously added log handlers
    logger.add(log_file, rotation="1 day", level="INFO")

def extract_data_mt5(from_date: str, mt5_credentials: dict) -> pd.DataFrame:
    """
    Extracts historical trade data from the MetaTrader 5 (MT5) platform using its API.

    This function connects to an MT5 account, retrieves historical trade data for symbols 
    containing "GBP", and returns the data as a pandas DataFrame. The time period for data 
    extraction spans from a predefined start date (from_date) to the current date and time.

    Args:
    from_date (str): A date string in the form of ('2023-09-24').
    mt5_credentials (dict): A dictionary with keys 'login', 'server', and 'password', providing 
                            the credentials for the MT5 account.

    Returns:
    pd.DataFrame: A DataFrame containing historical trade data, or None if the extraction fails.

    Raises:
    RuntimeError: If MT5 initialization or login fails.

    Example:
    >>> from_date = '2023-09-24'
    >>> mt5_credentials = {'login': 123456, 'server': 'YourServer', 'password': 'YourPassword'}
    >>> historical_data = extract_data_mt5(from_date, mt5_credentials)
    >>> print(historical_data)

    Note:
    The function relies on the MetaTrader5 (MT5) Python package and the `config` module for the 
    start date of the data extraction period. Ensure these dependencies are correctly set up 
    before using the function.
    """

    # Initialize MT5 connection
    if not mt5.initialize():
        logger.error("initialize() failed, error code: %s", mt5.last_error())
        raise RuntimeError("MT5 initialization failed")  
    
    try:
        # Log in to the MT5 terminal
        if not mt5.login(login=mt5_credentials['login'], server=mt5_credentials['server'], password=mt5_credentials['password']):
            logger.error("Login failed, error code: %s", mt5.last_error())
            raise RuntimeError("MT5 login failed")

        # Set display options for data retrieval
        pd.set_option('display.max_columns', 500)  # Number of columns to be displayed
        pd.set_option('display.width', 1500)       # Max table width to display

        # Log MetaTrader5 package information
        logger.info("MetaTrader5 package author: %s", mt5.__author__)
        logger.info("MetaTrader5 package version: %s", mt5.__version__)

        # Define the time period for data extraction
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.now()

        # Retrieve historical deals within the specified time period
        deals = mt5.history_deals_get(from_date, to_date)

        if deals is None:
            error_code = mt5.last_error()
            logger.warning("No deals found, error code = %d", error_code)
            return None
            
        elif len(deals) > 0:
            logger.info("history_deals_get(%s, %s) = %d deals", from_date, to_date, len(deals))
            # Create a DataFrame from the retrieved deals
            df = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df  
    
    finally:
        # Terminate the MT5 connection
        mt5.shutdown()


def data_transformation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms a DataFrame by splitting its 'time' column into separate 'date' and 'time' columns.

    This function assumes the 'time' column in the input DataFrame contains datetime information 
    in the format 'YYYY-MM-DD HH:MM:SS'. The function splits this column into two new columns: 
    'date' (containing 'YYYY-MM-DD') and 'time' (containing 'HH:MM:SS'). The original 'time' column 
    is converted to string type before the split for ease of processing.

    The new 'date' column is inserted into the original DataFrame, which is then returned with 
    the additional column.

    Args:
        df (pd.DataFrame): The original DataFrame containing at least a 'time' column with datetime information.

    Returns:
        pd.DataFrame: The transformed DataFrame with an additional 'date' column and the 'time' 
                      column split into date and time components.

    Raises:
        ValueError: If the input DataFrame does not contain a 'time' column.

    Example:
        >>> original_df = pd.DataFrame({'time': ['2022-01-01 12:00:00', '2022-01-02 13:00:00']})
        >>> transformed_df = data_transformation(original_df)
        >>> print(transformed_df)
    """

    # Check if 'time' column exists in the DataFrame
    if 'time' not in df.columns:
        raise ValueError("Input DataFrame does not contain a 'time' column")

    logger.info("Data transformation in process ....")

    # Convert 'time' column to string type to facilitate splitting
    df['time'] = df['time'].astype(str)

    # Split the 'time' column into 'date' and 'time' components
    date_time_split = df['time'].str.split(expand=True)
    date_time_split = date_time_split.rename(columns={0: "date", 1: "time"})
    
    # Insert the 'date' column into the DataFrame
    df.insert(2, 'date', date_time_split['date'])

    logger.info("Data transformation done!")
    
    # Return the DataFrame with the new 'date' column
    return df


def ETL(from_date, mt5_credentials: dict) -> pd.DataFrame:
    """
    Performs an Extract, Transform, Load (ETL) process on trading data from the MT5 platform.

    This function extracts trading data using the MetaTrader5 API, transforms the data,
    logs the process, saves the transformed data as a CSV file, and returns the data as a DataFrame.
    The data extraction is performed based on the provided MT5 credentials.

    Args:
    from_date (str): A date string in the form of ('2023-09-24').
    mt5_credentials (dict): A dictionary containing 'login', 'server', and 'password' for the MT5 account.

    Returns:
    pd.DataFrame: A DataFrame containing the transformed trading data, sorted by date in descending order.

    Example:
    >>> from_date = '2023-09-24'
    >>> mt5_credentials = {'login': 123456, 'server': 'YourServer', 'password': 'YourPassword'}
    >>> trading_data_df = ETL(from_date, mt5_credentials)
    >>> print(trading_data_df)
    """

    # Extract trading data from MT5
    df = extract_data_mt5(from_date, mt5_credentials)

    # Transform the extracted data
    df = data_transformation(df)

    # Log the start of data insertion into the database
    logger.info("Start inserting data into database")  # You might want to specify the database name if available

    # Log the completion of data extraction
    logger.info("Data extraction completed at {}".format(datetime.now()))

    # Log the successful completion of the program
    logger.info("Program completed successfully.")

    # Sort the DataFrame by date in descending order
    df = df.sort_values(by='date', ascending=False)

    # Save the DataFrame to a CSV file
    df.to_csv(config.FILE_PATH, index=False)

    # Return the transformed data as a DataFrame
    return df