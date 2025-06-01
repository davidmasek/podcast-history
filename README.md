# Podcast History

Sync and backup your podcast listening history.

Currently supports:
- Pocket Casts API
- manual input (JSON)

## Prerequisites

Put your Pocket Casts credentials into the [.env](.env) file:
```sh
EMAIL="foo@bar.com"
PASSWORD="..."
```

## Update History

By default history is stored inside the `data` folder.

```sh
# sync latest history
python3 main.py
```

## View History

Open [view.html](view.html) in a browser and choose [db.json](data/db.json) as the JSON file.


## Installation

Build with Python 3.10.

Install dependencies:
```sh
pip install -r requirements.txt
```

## Limitations

### Pocket Casts History Length

The Pocket Casts API currently returns only the last 100 items for your history. To bootstrap the database with older history you will need to provide it manually. https://github.com/furgoose/Pocket-Casts and https://github.com/donatj/pocketcasts-go provide some help but are not actively maintained. I've successfully used a combination of https://github.com/donatj/pocketcasts-go and custom Python scripts to get a reasonable starting point.

### Only Finished Episodes Are Tracked

This is intentional and by design. Tracking unfinished or in-progress episodes is not the goal of this project.

## Data Sources

### Pocket Casts API

The "unofficial" API `https://api.pocketcasts.com/user/history` endpoint is used. This is the endpoint used by the web and mobile clients.

## Manual Input

Currently all the data is stored in a simple JSON file. You can easily modify the file as needed.
