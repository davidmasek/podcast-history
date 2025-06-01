import json
from episode import Episode

DUMMY_EPISODES = [
    Episode(
        "how to test",
        "https://foo",
        "audio/mpeg",
        "1280",
        "2030-01-01",
        "abcd-1234",
        "Programming For Ducks",
        "Dr. Duck",
        "abce-5332",
        True,
    ),
]


def test_serialization():
    for ep in DUMMY_EPISODES:
        raw = json.dumps(ep.to_dict())
        decoded = Episode(**json.loads(raw))
        assert ep == decoded
