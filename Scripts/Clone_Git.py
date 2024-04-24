import subprocess
import os
import webbrowser

def clone_repo(git_command, target_dir):
    try:
        subprocess.run(git_command, check=True, shell=True)
        print("Repository successfully cloned.")
    except subprocess.CalledProcessError as e:
        print("Failed to clone repository:", e)

if __name__ == "__main__":
    token = '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'
    
    # Convert the repository SSH URL to HTTPS and include the token for authentication
    repo_url = "https://github.com/mdkamrulhasan/gvsu-gis.git"
    auth_repo_url = repo_url.replace('https://', f'https://{token}:x-oauth-basic@')
    
    # Specify the directory where you want to clone the repository
    target_dir = "C:\\Users\\nikhi\\Documents\\GitHub\\gvsu-gis"

    # Construct the full git command
    git_command = f"git clone {auth_repo_url} \"{target_dir}\""

    # Clone the repository and then run Master.py if successful
    clone_repo(git_command, target_dir)
