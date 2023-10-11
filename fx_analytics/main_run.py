
import subprocess
import os

# Set the current working directory to the folder containing your scripts
script_directory = os.path.dirname(os.path.abspath(__file__))

repo_directory = os.getcwd()
subprocess.run(['python', 'ETL.py'])

# run the app!
try:
    subprocess.run(['streamlit', 'run', 'app.py'])
except KeyboardInterrupt:
    print("Streamlit app was stopped.")

