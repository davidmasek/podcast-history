import logging
import json
import shutil
from pathlib import Path

from episode import Episode

logger = logging.getLogger(__name__)


class Store:
    episodes: list[Episode]

    def __init__(self, episodes: list[Episode]):
        self.episodes = episodes

    @staticmethod
    def from_file(file: Path) -> "Store":
        if not file.exists():
            raise ValueError(f"{file} does not exist")
        with open(file) as fh:
            logger.info(f"parsing episodes from {fh}")
            existing = json.load(fh)
        episodes = [Episode(**ep) for ep in existing]
        store = Store(episodes)
        logger.info(f"store loaded with {len(store.episodes)} episodes")
        return store

    def contains(self, episode: Episode) -> bool:
        for ep in self.episodes:
            if episode.uuid == ep.uuid:
                return True
        return False

    def add(self, episode: Episode) -> None:
        self.episodes.append(episode)

    def _save_to(self, file: Path) -> None:
        with open(file, "w") as fh:
            logger.info(f"Saving to {fh}")
            json.dump([ep.to_dict() for ep in self.episodes], fh, indent=2)

    def save(self, data_dir: Path) -> Path:
        data_dir.mkdir(parents=True, exist_ok=True)
        self._save_to(data_dir / "db-pre_autofill.json")
        self.autofill()

        try:
            shutil.copy2(data_dir / "db.json", data_dir / "db.bak.json")
        except FileNotFoundError:
            pass
        self._save_to(data_dir / "db.json")
        return data_dir / "db.json"

    def autofill(self) -> None:
        podcasts: dict[str, dict[str, list]] = {}
        for ep in self.episodes:
            if ep.podcast_uuid:
                if ep.podcast_uuid not in podcasts:
                    podcasts[ep.podcast_uuid] = {
                        "author": [],
                        "podcast_title": [],
                    }
                if (
                    ep.podcast_author
                    and ep.podcast_author not in podcasts[ep.podcast_uuid]["author"]
                ):
                    podcasts[ep.podcast_uuid]["author"].append(ep.podcast_author)
                if (
                    ep.podcast_title
                    and ep.podcast_title
                    not in podcasts[ep.podcast_uuid]["podcast_title"]
                ):
                    podcasts[ep.podcast_uuid]["podcast_title"].append(ep.podcast_title)

        for pod in podcasts.values():
            if len(pod["author"]) > 1:
                raise RuntimeError(
                    f"More than one author for pod {pod}, cannot autofill"
                )
            if len(pod["podcast_title"]) > 1:
                raise RuntimeError(
                    f"More than one title for pod {pod}, cannot autofill"
                )

        for ep in self.episodes:
            if ep.podcast_uuid and ep.podcast_uuid in podcasts:
                pod = podcasts[ep.podcast_uuid]
                if not ep.podcast_author and len(pod["author"]) == 1:
                    ep.podcast_author = pod["author"][0]
                    logger.info(
                        f"updated author for ep {ep.short_name()} to {ep.podcast_author}"
                    )
                if not ep.podcast_title and len(pod["podcast_title"]) == 1:
                    ep.podcast_title = pod["podcast_title"][0]
                    logger.info(
                        f"updated podcast title for ep {ep.short_name()} to {ep.podcast_title}"
                    )
