
import subprocess
import os
from typing import NoReturn

def run_app(script_path: str) -> NoReturn:
    """
    Executes specific Python scripts located in a given directory.

    This function first changes the current working directory to the one specified,
    then executes an ETL.py script, and finally runs a Streamlit application.
    If the Streamlit application is stopped by the user, a message is printed.

    Args:
    script_path (str): The file path of the script directory.

    Raises:
    KeyboardInterrupt: If the Streamlit application is stopped by the user.

    Returns:
    NoReturn: This function does not return anything, it's meant for script execution only.
    """

    # Set the current working directory to the folder containing your scripts
    os.chdir(script_path)

    # Execute the ETL script
    subprocess.run(['python', 'ETL.py'])

    # Run the Streamlit app
    try:
        subprocess.run(['streamlit', 'run', 'app.py'])
    except KeyboardInterrupt:
        print("Streamlit app was stopped.")


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    run_app(script_directory)


