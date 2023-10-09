import subprocess

def create_environment():

    # Define the name of the virtual environment
    venv_name = "app"  # Change this to your desired environment name

    # Create the virtual environment
    subprocess.run(["python3", "-m", "venv", venv_name])

    # Activate the virtual environment
    activate_script = f"./{venv_name}/bin/activate"
    subprocess.run(["source", activate_script], shell=True) 

    # Install requirements from 'requirements.txt'
    subprocess.run(["pip", "install", "-r", "requirements.txt", "--user"])

    # Deactivate the virtual environment
    # subprocess.run(["deactivate"], shell=True)

    # print("Virtual environment created and requirements installed.")