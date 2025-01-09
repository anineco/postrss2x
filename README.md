# postrss2x
Automatically post articles from RSS to X (Twitter)

## 概要
RSS からウェブサイトの更新情報を取得し、X（Twetter）に自動投稿するプログラム。RSS 1.0 と RSS 2.0 に対応。起動毎に、未投稿で公開日が最も古い情報を1件投稿する。

## インストール方法
次のプログラムとモジュールが必要。
- Python 3.8 以上
- tweepy 4.14.0
- sqlite3

tweepy モジュールがない場合は、次のコマンドでインストールする。
```bash
$ pip install tweepy
```

なお、tweepy 4.14.0 は Python 3.13 では動作しないので注意。

次に`config_dist.py`のファイル名を`config.py`に変えて、`postrss2x.py`と同じディレクトリに設置する。
[X Developer Portal](https://developer.x.com/en/portal/dashboard) から、X API v2 の認証情報（Freeプランで可）
- API Key
- API Secret
- ACCESS Token (Read and Write permission)
- ACCESS Secret

を取得し、RSSのURLとともに`config.py`に記載する。

投稿メッセージは、`config.py`の下記の箇所のテンプレートから作成されるので、適宜、変更する。`{title}`は記事のタイトル、`{link}`は記事のURLに置き換えられる。
```python
MESSAGE = "【新着情報】{title}\n{link}"
```

## 利用方法
次のようにコマンドを実行する。
```bash
$ ./postrss2x.py [-p] [-l] [-m]
```
オプションの説明
- `-p` ：投稿を実行。このオプションを指定しない場合、投稿は実行されない。
- `-l` ：更新情報（公開日、URL、タイトル）と投稿IDの一覧を表示。投稿IDが -1 の場合は未投稿であることを表す。
- `-m` ：未投稿の更新情報の投稿IDをすべて 0 に書き換えて、投稿済と見做すようにする。

## 制限事項
- Freeプランの場合、毎月の投稿数の上限は500件である。
