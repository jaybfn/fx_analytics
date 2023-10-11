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
from main_functions import ETL
#from fx_analytics import config




if __name__ == '__main__':

    mt5_credentials = {'login': 7055689, 'server':'ICMarketsSC-MT5-2','password':'4KCEG3Kc'}
    from_date = '2023-09-20'
    df = ETL(from_date, mt5_credentials)
    print(df.head())
    
