

import fx_analytics
import os
from fx_analytics import ETL
from fx_analytics import app as app

# uncomment and run this if you have mt5 terminal installed!
# df = ETL.load()
# print(df.head())

# check the app with the example data!
os.system("streamlit run fx_analytics/app.py")

