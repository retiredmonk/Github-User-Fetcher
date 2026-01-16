import requests, logging, os
from typing import Any, Dict
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
log_path = Path("logs/github_info_fetcher.log")
log_path.parent.mkdir(exist_ok=True)
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=" %(asctime)s - %(levelname)s - %(message)s")

api_key = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

if not api_key:
    logging.critical("GITHUB_PERSONAL_ACCESS_TOKEN is not set")
    print("Provide a GitHub Personal Access Token")
    raise SystemExit(1)

base_url = "https://api.github.com"
timeout = 10

def build_url (username: str) -> str:
    return f"{base_url}/users/{username.strip()}"

def get_headers () -> dict:
    return {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github_info_fetcher/1.0",
        "Authorization": f"Bearer {api_key}"
    }

def safe(value: Any) -> str:
    return str(value) if value not in (None, "") else "Not available"


def fetch_user (url: str) -> Dict[str, Any]:

    try:
        response = requests.get(url, headers=get_headers(), timeout=timeout)

        if response.status_code == 404:
            raise RuntimeError("User not found")
        elif response.status_code == 403:
            raise RuntimeError("Rate limit exceeded or invalid token")

        logging.info("Status Code: %s", response.status_code)
        response.raise_for_status()

        data = response.json()
        return data

    except requests.exceptions.Timeout as e:
        logging.error(e)
        raise RuntimeError ("Request timed out")
    except requests.exceptions.TooManyRedirects as e:
        logging.error(e)
        raise RuntimeError ("Too many redirects")
    except requests.exceptions.RequestException as e:
        logging.error(e)
        raise RuntimeError (f"Request failed: {e}")
    except ValueError as e:
        logging.error(e)
        raise RuntimeError ("Invalid JSON response from API")

def display_user (data: Dict[str, Any]) -> None:
    logging.info("Fetched user: %s", data.get("login"))
    print("\n===== GitHub User Info =====")
    print(f"Username       : {safe(data.get('login'))}\n")
    print(f"Name           : {safe(data.get('name'))}\n")
    print(f"Bio            : {safe(data.get('bio'))}\n")
    print(f"Public Repos   : {safe(data.get('public_repos'))}\n")
    print(f"Followers      : {safe(data.get('followers'))}\n")
    print(f"Following      : {safe(data.get('following'))}\n")
    print(f"Profile URL    : {safe(data.get('html_url'))}\n")
    print("===========================\n")

def main() -> None:

    user_name = input("Enter GitHub Username: ")

    if not user_name:
        logging.critical("Invalid GitHub Username")
        print("Provide a Valid GitHub Username")
        return

    url = build_url(user_name)

    try:
        data = fetch_user(url)
        display_user(data)
    except RuntimeError as e:
        logging.error(e)
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

