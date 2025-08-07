import requests

# Base URL of the website under test
JOBGENIOUS_URL = "https://www.gojobgenius.com/"

def is_url_reachable(url):
    """
    Checks whether the given URL is reachable by sending a HEAD request.
    Returns True if reachable, else False.
    """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
