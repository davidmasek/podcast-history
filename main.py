import logging
from pathlib import Path

from store import Store
import history_source

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "data"


def main():
    store = Store.from_file(DATA_DIR / "db.json")
    history_source.update_store(store)
    store.save(DATA_DIR)


if __name__ == "__main__":
    main()
