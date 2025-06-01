import requests
from pathlib import Path
import logging

from env_manager import get_credentials

TOKEN_FILE = Path("token.txt")

logger = logging.getLogger(__name__)


def get_token() -> str:
    try:
        logger.info(f"Loading token from {TOKEN_FILE}")
        token = TOKEN_FILE.read_text().strip()
    except FileNotFoundError:
        token = ""
        logger.info("Did not find file with token")

    if not token:
        email, password = get_credentials()
        token = _get_token(email, password)
        TOKEN_FILE.write_text(token)

    return token


def _get_token(email: str, password: str) -> str:
    logger.info("Getting token from API")
    resp = requests.post(
        "https://api.pocketcasts.com/user/login",
        {
            "email": email,
            "password": password,
            "scope": "webplayer",
        },
    )
    resp.raise_for_status()
    data = resp.json()
    token = data["token"]
    if not token:
        raise RuntimeError(f"Token not found in response json {data}")
    return token


if __name__ == "__main__":
    token = get_token()
    print(token)
