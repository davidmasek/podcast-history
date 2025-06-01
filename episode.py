import dataclasses
from dataclasses import dataclass


@dataclass
class Episode:
    """
    Example:
    {
        "title": "Fooniverse - Questions from the Patrons 2",
        "url": "https://.../...",
        "file_type": "audio/mpeg",
        "file_size": 134369408,
        "published": "2022-10-06T04:00:05Z",
        "uuid": "50285cd6-2971-41b2-9eec-ba97864d5e1a",
        "podcast_title": "Hello from the Magic Tavern BONUS + AD FREE",
        "podcast_author": "Magic Tavern LLC",
        "podcast_uuid": "ef315360-84f1-013d-e49e-02bf0009cf0d",
        "finished": true
    }
    """

    title: str
    url: str
    file_type: str
    file_size: str
    published: str
    uuid: str
    podcast_title: str
    podcast_author: str
    podcast_uuid: str
    finished: bool

    def short_name(self) -> str:
        return f"Episode({self.title[:20]}; {self.uuid})"

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)
