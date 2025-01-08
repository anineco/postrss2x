# postrss2x
Automatically post articles from RSS 2.0 to X (Twitter)

## 概要
RSS 2.0からウェブサイトの更新情報を取得し、X（Twetter）に自動投稿するプログラム。起動毎に、未投稿で公開日の古い情報から投稿する。

## インストール方法
次のプログラムとモジュールが必要。
- Python 3.x
- tweepy 4.14.0
- sqlite3

tweepy モジュールがない場合は、次のコマンドでインストールする。
```bash
$ pip install tweepy
```

なお、現時点（2025-01-09）で、Python 3.13.xでは tweepy が動作しないので注意。

次に`config_dist.py`のファイル名を`config.py`に変えて、`postrss2x.py`と同じディレクトリに設置する。
[X Developer Portal](https://developer.x.com/en/portal/dashboard) から、X API v2 の認証情報（Freeプランで可）
- API Key
- API Secret
- ACCESS Token (Read and Write permission)
- ACCESS Secret

を取得し、RSSのURLとともに`config.py`に記載する。

## 利用方法
次のようにコマンドを実行する。
```bash
$ ./postrss2x.py [-p] [-l] [-m]
```
オプションの説明
- `-p` ：投稿を実行。このオプションを指定しない場合、投稿は実行されない。
- `-l` ：更新情報（公開日、URL、タイトル）と投稿IDの一覧を表示。投稿IDが-1の場合は未投稿であることを表す。
- `-m` ：未投稿の更新情報の投稿IDをすべて0に書き換えて、投稿済と見做すようにする。

## 制限事項
- 公開日はRSS 2.0の`dc:date`要素から取得しているので、この要素が欠けている場合、正常に動作しない。
- Freeプランの場合、毎月、最大500件までの投稿が可能。

## TODO
- RSS 2.0 で`dc:date`要素がない場合、`pubData`要素から公開日を取得するようにする。
- RSS 1.0 対応。
