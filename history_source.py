import requests
from pathlib import Path
import logging

from pocket_auth import get_token
from episode import Episode
from store import Store

STATUS_FINISHED = 3

DATA_DIR = Path(__file__).parent / "data"

logger = logging.getLogger(__name__)


def get_history(token: str) -> dict:
    resp = requests.post(
        "https://api.pocketcasts.com/user/history",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    resp.raise_for_status()
    return resp.json()


def parse_history(raw_history: dict) -> list[Episode]:
    episodes = []
    for episode_raw in raw_history["episodes"]:
        finished = episode_raw["playingStatus"] == STATUS_FINISHED
        # we only care about finished episodes
        if not finished:
            continue
        try:
            # one of those should be present
            title = episode_raw.get("episodeTitle", episode_raw["title"])
            episode = Episode(
                title,
                episode_raw["url"],
                episode_raw["fileType"],
                episode_raw["size"],
                episode_raw["published"],
                episode_raw["uuid"],
                episode_raw["podcastTitle"],
                episode_raw["author"],
                episode_raw["podcastUuid"],
                finished,
            )
        except KeyError:
            logger.error(f"failed to parse {episode_raw}")
            raise

        episodes.append(episode)
    return episodes


def update_store(store: Store) -> None:
    token = get_token()
    raw_history = get_history(token)
    if len(raw_history["episodes"]) == 0:
        raise RuntimeError("No episodes found in history!")

    episodes = parse_history(raw_history)

    for episode in episodes:
        if not store.contains(episode):
            logger.info(f"adding new played episode {episode.short_name()}")
            store.add(episode)
