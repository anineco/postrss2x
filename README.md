# postrss2x
Automatically post articles from RSS to X (Twitter)

[日本語 (Japanese)](blob/main/README.jp.md)

## Overview
This program fetches updates from RSS feeds and automatically posts them to X (formerly Twitter). It supports RSS 1.0 and RSS 2.0. Designed to be executed periodically via cron, the program posts updates from the oldest unpublished entry up to a specified number of posts during each execution.

## Installation
The following programs and modules are required:
- Python 3.8 or higher
- tweepy 4.14.0
- sqlite3

To install the tweepy module, run the following command:
```bash
$ pip install tweepy
```

Note: tweepy 4.14.0 is not compatible with Python 3.13.

Rename the `config_dist.py` file to `config.py` and place it in the same directory as `postrss2x.py`.
Obtain the following X API v2 credentials (available under Free plan) from the [X Developer Portal](https://developer.x.com/en/portal/dashboard):
- API Key
- API Secret
- ACCESS Token (Read and Write permission)
- ACCESS Secret

Add these credentials and the RSS feed URL to the `config.py` file.

The posting message is generated from the following template in `config.py`. You can modify it as needed. `{title}` will be replaced with the article title, and `{link}` will be replaced with the article URL:
```python
MESSAGE = "Updates: {title}\n{link}"
```

Set the following parameters in `config.py`:
- `MAX_RECORDS`: The maximum number of records to retain in the database.
- `MAX_POSTS`: The maximum number of posts per execution.

Ensure that the values satisfy the condition `MAX_RECORDS > N - MAX_POSTS`, where `N` is the number of new entries fetched from the RSS feed, to handle variations in `N` appropriately.

## Usage
Run the program with the following command:
```bash
$ ./postrss2x.py [-p] [-l] [-m]
```

Options:
- `-p`: Execute posting. If this option is not specified, no posts will be made.
- `-l`: Display a list of updates (publication date, URL, title) and post IDs. A post ID of -1 indicates the update has not been posted.
- `-m`: Set the post ID of all unpublished updates to 0, marking them as posted.

## Limitations
- The Free plan allows a maximum of 500 posts per month.
