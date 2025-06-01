import logging
from pathlib import Path
import argparse
import datetime
import subprocess

from store import Store
import history_source
from env_manager import CredentialsNotProvidedException

logging.basicConfig(level=logging.INFO)

DEFAULT_DATA_DIR = Path(__file__).parent / "data"


logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
parser.add_argument("--rclone-remote", type=str, default="")


def main():
    args = parser.parse_args()
    db_file = args.data_dir / "db.json"
    if db_file.exists():
        store = Store.from_file(args.data_dir / "db.json")
    else:
        store = Store([])
    try:
        history_source.update_store(store)
    except CredentialsNotProvidedException:
        logger.error("Credentials not provided. Set EMAIL and PASSWORD env variables or provide .env file.")
        exit(1)
    db_file = store.save(args.data_dir)
    remote = args.rclone_remote
    if remote:
        today = datetime.date.today().isoformat()
        rclone_cmd = [
            "rclone",
            "copy",
            str(db_file),
            f"{remote}:podcast-history/current/",
            "--backup-dir",
            f"{remote}:podcast-history/archive/",
            "--suffix",
            f".{today}",
        ]
        try:
            logger.info(f"Running {rclone_cmd}")
            subprocess.run(rclone_cmd, check=True)
        except subprocess.CalledProcessError as exc:
            logger.error(f"rclone upload failed with exit code {exc.returncode}")
            raise


if __name__ == "__main__":
    main()
