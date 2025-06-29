import os
from pathlib import Path
from dotenv import dotenv_values

class CredentialsNotProvidedException(Exception):
    pass

def get_credentials() -> tuple[str, str]:
    username = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")
    env_file = Path(".env")
    if env_file.exists():
        config = dotenv_values(env_file)
        if not username and config.get("EMAIL", ""):
            username = config["EMAIL"]
        if not password and config.get("PASSWORD", ""):
            password = config["PASSWORD"]

    if not username:
        raise CredentialsNotProvidedException("Cannot find EMAIL")
    if not password:
        raise CredentialsNotProvidedException("Cannot find PASSWORD")
    return username, password
