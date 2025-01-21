#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Automatically post articles from RSS to X (Twitter)

import os
from email.utils import parsedate_to_datetime
import sqlite3
import sys
import xml.etree.ElementTree as ET

import requests
import tweepy

import config # add your API keys and RSS URL to config.py

# command line options
post = False
disp = False
mark = False
for arg in sys.argv[1:]:
    if arg == "-p":
        post = True # post articles
    elif arg == "-l":
        disp = True # list articles
    elif arg == "-m":
        mark = True # mark all articles as posted
    else:
        print(f"Usage: {sys.argv[0]} [-p] [-l] [-m]")
        sys.exit(1)

# X API v2 credentials
client = tweepy.Client(
    consumer_key=config.API_KEY,
    consumer_secret=config.API_KEY_SECRET,
    access_token=config.ACCESS_TOKEN,
    access_token_secret=config.ACCESS_TOKEN_SECRET
)

# database for recording posted articles
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
os.chdir(script_dir)

connection = sqlite3.connect(config.DATABASE)
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS record (
    link TEXT PRIMARY KEY, -- URL of the article
    title TEXT NOT NULL,   -- title
    date TEXT NOT NULL,    -- publication date (ISO8601)
    post_id INTEGER DEFAULT -1  -- post ID
)
""")
connection.commit()

# retrieve updated articles from RSS
response = requests.get(config.RSS_URL)
if not response.status_code == 200:
    print("Can't get RSS: ", response.status_code)
    sys.exit(1)

# parse RSS feed and insert URL, title, and publication date into the database
root = ET.fromstring(response.content)
namespaces = { "dc": "http://purl.org/dc/elements/1.1/"}
version = root.get("version")
if not version == "2.0":
    # RSS 1.0
    namespaces[""] = "http://purl.org/rss/1.0/"
for item in root.findall(".//item", namespaces):
    link = item.find("link", namespaces).text   # URL of the article
    title = item.find("title", namespaces).text # title
    if version == "2.0" and (p := item.find("pubDate", namespaces)) is not None:
        date = parsedate_to_datetime(p.text).isoformat()
    else:
        date = item.find("dc:date", namespaces).text # publication date (ISO8601)
    cursor.execute("INSERT OR IGNORE INTO record (link,title,date) VALUES (?,?,?)", (link, title, date))
    connection.commit()

# delete old records except for the latest MAX_RECORDS
cursor.execute("""
DELETE FROM record WHERE link NOT IN (
    SELECT link
    FROM record
    ORDER BY date DESC
    LIMIT ?
)
""", (config.MAX_RECORDS,))
connection.commit()

if mark:
    # mark all articles as posted
    cursor.execute("UPDATE record SET post_id=0 WHERE post_id<0")
    connection.commit()

if disp:
    # list all articles in the database
    cursor.execute("SELECT link,title,date,post_id FROM record ORDER BY date ASC")
    for link, title, date, post_id in cursor.fetchall():
        print(date, link, title, f"({post_id})")

# find articles not yet posted ordered by publication date
cursor.execute("SELECT link,title FROM record WHERE post_id<0 ORDER BY date ASC LIMIT ?", (config.MAX_POSTS,))
for link, title in cursor.fetchall():
    message = config.MESSAGE.format(link=link, title=title)
    print(message) # for debug
    if post:
        try:
            response = client.create_tweet(text=message)
        except Exception as e:
            print(f"Failed to post. Error: {e}") 
            sys.exit(1)
        post_id = response.data["id"]
        print(f"Success post: {post_id}")
        cursor.execute("UPDATE record SET post_id=? WHERE link=?", (post_id, link))
        connection.commit()

connection.close()
#__END__
