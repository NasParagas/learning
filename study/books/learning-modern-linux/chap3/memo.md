# shellとscript

## 用語

- **Shell**はterminal内で動作するもの
  - terminal: xterm, Gnome terminaor, kitty, warp, wezterm...
    - terminal == terminal emulator == soft terminal
  - shell: sh, bash, fish...
- `echo $0`,`echo $SHELL`等で自分がどのshellを使っているかを確認できる
  - (TODO: $0でなんで取れる？)

### stream

- Input streamとOutput streamがある(I/O)
- shellはすべてのprocessにI/O用の3つのfile descriptorを用意している
  - stdin(0): 標準入力
  - stdin(1): 標準入力
  - stdin(2): 標準エラー出力
- デフォルトでは0はキーボード、1,2はスクリーンに接続されている
- このstreamをredirectすることで、スクリーンではなくファイル等に出力することができる
- processのoutput streamをredirectするには`$FD>`と`<$FD`を使う
  - 例えば`2>`はstrdrrをredirectする事を意味する
  - `$FD`のデフォルト値は1であるため、`1>`と`>`は同じ意味
  - `&>`でstdoutとstderr両方をredirectできる
  - outputが不要な場合には`&> /dev/null`を使用する
- 例

```sh
curl https://httpbin.org/get &> /tmp/curl-tmp.md
cat /tmp/curl-tmp.md
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed
100    256 100    256   0      0    367      0                              0
{
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Host": "httpbin.org", 
    "User-Agent": "curl/8.18.0", 
    "X-Amzn-Trace-Id": "Root=1-6a49c379-3a3e57644f66c26120fc426d"
  }, 
  "origin": "133.32.226.151", 
  "url": "https://httpbin.org/get"
}

curl https://httpbin.org/get > /tmp/curl-stdout.md 2> /tmp/curl-stderr.md

cat /tmp/curl-stdout.md 
{
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Host": "httpbin.org", 
    "User-Agent": "curl/8.18.0", 
    "X-Amzn-Trace-Id": "Root=1-6a49c3dc-12833d5a2b6ef98d3695e09e"
  }, 
  "origin": "133.32.226.151", 
  "url": "https://httpbin.org/get"
}

cat /tmp/curl-stderr.md 
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed
100    256 100    256   0      0    342      0                              0

# C-dでキャプチャ停止
cat > /tmp/input.md
konnnitiha     
konnbannha 
aa

cat /tmp/input.md 
konnnitiha
konnbannha 
aa

# stdinから読み込んだ文字を置き換えるcommand. ここではalphabetを大文字から小文字へ変換している
tr < /tmp/curl-stderr.md [A-Z] [a-z]
  % total    % received % xferd  average speed  time    time    time   current
                                 dload  upload  total   spent   left   speed
100    256 100    256   0      0    342      0                              0
```

- shellでは以下のような特殊文字が解釈される
  - `&`: コマンドの最後に置くとそのコマンドはバックグラウンドで実行される
  - `\`: 次の行にもcommandを続けられる
  - `|`: あるprocessのstdoutと次のprocessのstdinを接続する(`history | grep "ssh"`とか)

### 変数

- 環境変数
  - shell全体の設定。`env`で一覧表示できる
- shell変数
  - 現在実行中のshellでのみ有効。shellから起動されるchild processには継承されない
  - `set`で設定する(TODO:??)
- 変数をいじる例

```zsh

```
