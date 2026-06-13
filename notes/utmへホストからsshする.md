- UTMの設定から共有ネットワークにする
- ゲストubuntu側へsshdをインストール

```sh
sudo apt install openssh-server
sudo systemctl enable --now ssh   # 起動 + 自動起動
systemctl status ssh              # active (running) を確認
```

- `ip addr`でip確認し`ssh user@host`

