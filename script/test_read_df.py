import pandas as pd
import os
import pytest

# Define a function to check if a DataFrame exists and contains data
def check_dataframe_exists_and_not_empty(df):
    # Check if the DataFrame is not None
    assert df is not None
    
    # Check if the DataFrame is not empty (contains at least one row)
    assert not df.empty

# Define a test function
def test_check_dataframe_exists_and_not_empty():
    # Define the path to the CSV file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, 'fx_history.csv')
    
    # Check if the CSV file exists
    assert os.path.isfile(csv_file_path)
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Call the function to check if the DataFrame exists and is not empty
    check_dataframe_exists_and_not_empty(df)

# Run the tests with pytest
if __name__ == '__main__':
    pytest.main()

