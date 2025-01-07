#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tweepy

import config # config.py に認証情報を記述

# 認証設定
client = tweepy.Client(
    consumer_key=config.API_KEY,
    consumer_secret=config.API_KEY_SECRET,
    access_token=config.ACCESS_TOKEN,
    access_token_secret=config.ACCESS_TOKEN_SECRET
)

# 認証
try:
    # 認証が成功したか確認するために自分のユーザー情報を取得
    user = client.get_me()
    print("認証成功！ユーザー名:", user.data['username'])
except tweepy.TweepyException as e:
    # エラーハンドリング（認証失敗の場合）
    print(f"認証エラー： {e}")
    sys.exit(1)

# 投稿
try:
    response = client.create_tweet(text="PythonからX API v2で投稿しています！")
    print(f"投稿成功！ID: {response.data['id']}")
except Exception as e:
    print(f"投稿エラー: {e}")
    sys.exit(1)

# __END__
