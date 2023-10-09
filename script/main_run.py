
import subprocess
import os
 
# Set the current working directory to the folder containing your scripts
script_directory = os.path.dirname(os.path.abspath(__file__))

# message for the git commit!
msg = "updated new CSV file!"

# Set the environment variable for SSH authentication
#os.environ['GIT_SSH_COMMAND'] =  'ssh -i /c/Users/Asus/.ssh/id_rsa -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
repo_directory = os.getcwd()
subprocess.run(['python', 'ETL.py'])
# Set up Git credential helper
subprocess.run(["git", "config", "--global", "credential.helper", "store"])

# Add and commit your changes
subprocess.run(["git", "add", "."], cwd=repo_directory)
subprocess.run(["git", "commit", "-m", msg], cwd=repo_directory)

# Push without being prompted for credentials
subprocess.run(["git", "push"], cwd=repo_directory)

# run the app!
# subprocess.run(['streamlit', 'run', 'app.py'])
