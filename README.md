
# Pub/Sub Learn

おもむろに Pub/Sub パターンを学んだメモ。いろんな書籍やネットの情報を元に自分なりに使いやすいと思った設計で作ってみる

## Infrastructure

メッセージを送信するためのインフラ層の実装。

メール送信、Slack、Webダッシュボード、ログ出力などの実装を想定。

## Subscribers

抽象クラスとして `Subscriber` を用意。
`Subscriber` は `Infrastructure` に実際の送信処理を委譲している。

## NotificationService

`Subscriber` と `Infrastructure` を組み合わせて、メッセージを送信するサービスを提供する。

## main.py

API エンドポイント。


---

## その他

### Repository

実際のプロダクトだと、どのユーザー、どのプロジェクト、どんな通知イベントを送信するかなどをDBに保存する必要があるので、それらを扱う Repository クラスを作成する。
今回はJSONで雑に実装する。
