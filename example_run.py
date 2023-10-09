

import fx_analytics
import os
from fx_analytics import ETL
from fx_analytics import app as app


df = ETL.load()
print(df.head())


os.system("streamlit run fx_analytics/app.py")

