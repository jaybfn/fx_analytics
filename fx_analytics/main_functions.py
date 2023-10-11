import os
import MetaTrader5 as mt5
from datetime import datetime, date
from typing import List, Dict
import pandas as pd
from loguru import logger
from .credential import mt5_credentials
import plotly.express as px
import plotly.graph_objects as go
from . import config


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

def extract_data_mt5(mt5_credentials: dict) -> pd.DataFrame:
    
    """This function extracts historical trade data from the mt5 platform using MT5 API!"""

    # establish MetaTrader 5 connection to a specified trading account

    if not mt5.initialize():
        logger.info("initialize() failed, error code: %s",mt5.last_error())
        return None
    
    try:

        if not mt5.login(login=mt5_credentials['login'], server=mt5_credentials['server'],password=mt5_credentials['password']):
            logger.error("Login failed, error code: %s", mt5.last_error())
            return None
    
        pd.set_option('display.max_columns', 500) # number of columns to be displayed
        pd.set_option('display.width', 1500)      # max table width to display

        # display data on the MetaTrader 5 package
        logger.info("MetaTrader5 package author: %s", mt5.__author__)
        logger.info("MetaTrader5 package version: %s", mt5.__version__)

        from_date=config.DATETIME
        to_date=datetime.now()

        # get deals for symbols whose names contain "GBP" within a specified interval
        deals=mt5.history_deals_get(from_date, to_date)

        if deals==None:
            error_code = mt5.last_error()
            logger.warning("No deals found, error code = %d", error_code)
            
        elif len(deals)> 0:
            logger.info("history_deals_get(%s, %s) = %d", from_date, to_date, len(deals))
            # display these deals as a table using pandas.DataFrame
            df=pd.DataFrame(list(deals),columns=deals[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
                #logging.info("\n%s", df)
            #return df
        return df  
    
    finally:
        # shut down connection to the MetaTrader 5 terminal
        mt5.shutdown()


def data_transformation(df: pd.DataFrame) -> pd.DataFrame:
 
    """
    Split a DataFrame's 'time' column into separate 'date' and 'time' columns,
    and create a new DataFrame with selected columns for report analysis.

    Args:
        df (pd.DataFrame): Input DataFrame containing a 'time' column.
    return:
        pd.DataFrame: A new DataFrame with 'date' and selected columns for analysis.
    """

    logger.info("Data transformation in process ....")
    # Convert 'time' column to string type
    df['time'] = df['time'].astype(str)

    # Split the 'time' column into 'date' and 'time'
    date_time_split = df['time'].str.split(expand=True)
    date_time_split = date_time_split.rename(columns={0: "date", 1: "time"})
    df.insert(2, 'date', date_time_split['date'])

    # Create a new DataFrame with selected columns for analysis
    selected_columns = ['date', 'type', 'volume','position_id','price','commission', 'swap', 'profit', 'fee', 'symbol']
    df_report_analysis = df[selected_columns]
    #df_report_analysis = df.copy()
    logger.info("Data transformation done!")
    return df_report_analysis
