"""
    The code is used to extract data from MetaTrader5 using the "MetaTrader5" library 
    and store the data into a database using SQLAlchemy. The code uses a bulk insert 
    approach to insert the data more efficiently into the database. It also logs the 
    program's execution time and status to a log file.#

"""
# import sys
# sys.path.append('script/')
import pandas as pd
import numpy as np
from loguru import logger
import MetaTrader5 as mt5
from main_functions import *
import config as config

def data_extract_transform()-> pd.DataFrame:
    """
    Extracts data from the MetaTrader5 platform, performs data transformation, and returns a DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted and transformed data.
    """
    # Get data from the MT5 platform using the get_mt5_data function
 
    df = extract_data_mt5()
    df = data_transformation(df)
    
    return df
    

def load() -> pd.DataFrame:
    """
    Loads data by calling data_extract_transform, logs the start and completion of data insertion,
    and returns a DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.
    """

    df = data_extract_transform()
    # Log the start of data insertion into the database
    logger.info("Start inserting data into {}")
    # Log the completion of data insertion and the successful completion of the program
    logger.info("Data extraction completed at {}".format(datetime.now()))
    logger.info("Program completed successfully.")
    df = df.sort_values(by = 'date', ascending=False)
    df.to_csv(config.FILE_PATH, index  = False)
    return df

if __name__ == '__main__':
    
    setup_logging(config.LOG_PATH)

    load()
