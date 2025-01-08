#!/usr/bin/env python
# -*- coding: utf-8 -*-

# RSS 2.0からX(Twetter)に記事を自動投稿する

import os
import sqlite3
import sys
import xml.etree.ElementTree as ET

import requests
import tweepy

import config # config.py に認証情報を記述

# コマンドライン引数
post = False
disp = False
mark = False
for arg in sys.argv[1:]:
    if arg == "-p":
        post = True # Xに投稿する
    elif arg == "-l":
        disp = True # 記事の一覧を表示する
    elif arg == "-m":
        mark = True # 記事を全て投稿済にする
    else:
        print(f"Usage: {sys.argv[0]} [-p] [-l] [-m]")
        sys.exit(1)

# X API v2 認証設定
client = tweepy.Client(
    consumer_key=config.API_KEY,
    consumer_secret=config.API_KEY_SECRET,
    access_token=config.ACCESS_TOKEN,
    access_token_secret=config.ACCESS_TOKEN_SECRET
)

# 配信記録データベース
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
os.chdir(script_dir)

connection = sqlite3.connect(config.DATABASE)
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS record (
    link TEXT PRIMARY KEY, -- 記事のURL
    title TEXT NOT NULL,   -- タイトル
    date TEXT NOT NULL,    -- 公開日（YYYY-MM-DD）
    post_id INTEGER DEFAULT -1  -- 投稿ID
)
""")

# RSSを取得
response = requests.get(config.RSS_URL)
if not response.status_code == 200:
    print("Can't get RSS: ", response.status_code)
    sys.exit(1)

# RSSを解析して、記事情報をデータベースに保存
root = ET.fromstring(response.content)
namespaces = { "dc": "http://purl.org/dc/elements/1.1/" }

for item in root.findall(".//item", namespaces):
    link = item.find("link", namespaces).text    # 記事のURL
    title = item.find("title", namespaces).text  # タイトル
    date = item.find("dc:date", namespaces).text # 公開日
    cursor.execute("INSERT OR IGNORE INTO record (link,title,date) VALUES (?,?,?)", (link, title, date))

# 日付順で上位10を残して削除
cursor.execute("""
DELETE FROM record WHERE link NOT IN (
    SELECT link
    FROM record
    ORDER BY date DESC
    LIMIT 10
)
""")

# 記事を全て投稿済にする
if mark:
    cursor.execute("UPDATE record SET post_id=0 WHERE post_id<0")

if disp:
    # 一覧表示
    cursor.execute("SELECT link,title,date,post_id FROM record ORDER BY date ASC")
    for link, title, date, post_id in cursor.fetchall():
        print(date, link, title, f"({post_id})")

# 未投稿で最も古い記録を取得
cursor.execute("SELECT link,title FROM record WHERE post_id<0 ORDER BY date ASC LIMIT 1")
row = cursor.fetchone()
if row is not None:
    link = row[0]
    title = row[1]
    message = f"【山行記録】{title}\n{link}" # 🔖 投稿メッセージ
    print(message)
    if post:
        try:
            response = client.create_tweet(text=message)
        except Exception as e:
            print(f"投稿エラー: {e}")
            sys.exit(1)
        post_id = response.data["id"]
        print(f"投稿成功: {post_id}")
        cursor.execute("UPDATE record SET post_id=? WHERE link=?", (post_id, link))

connection.commit()
connection.close()
#__END__
