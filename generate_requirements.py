import subprocess

# Generate the requirements.txt file
subprocess.run(["pipenv", "lock", "-r", "--dev"], capture_output=True, text=True)

# Move the generated Pipfile.lock to requirements.txt
subprocess.run(["mv", "Pipfile.lock", "requirements.txt"])
