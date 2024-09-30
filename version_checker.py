import requests
from packaging import version

def check_for_updates(current_version):
    try:
        # Fetch the latest release information from your GitHub repository
        response = requests.get("https://api.github.com/repos/YourUsername/EldenRingModUpdater/releases/latest")
        latest_release = response.json()
        
        latest_version = latest_version = latest_release['tag_name'].lstrip('v')
        
        # Compare versions
        if version.parse(latest_version) > version.parse(current_version):
            return True, latest_version, latest_release['assets'][0]['browser_download_url']
        else:
            return False, None, None
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return False, None, None