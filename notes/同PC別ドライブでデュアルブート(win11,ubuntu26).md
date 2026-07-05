before  
SSDにシステムファイルがあって、HDDを外部記憶装置として使っているwindow11

after  
SSDはwindows11, HDDはubuntu26.04

同ディスクでパーティション分けて...みたいなのはこの記事は対象外です

## 注意点

- windows11を使っている時にHDDに入れていたデータは全て消えますので、適宜SSDに移しましょう

## そもそも

この方式をとる場合でも、いくつかやり方が分かれます

- ブートローダーを共有
  - ここでは細かい話まではしないですが、OS(windows11とかubuntuとか)をメモリに展開するために、最初にブートローダーと言うものが起動されます。それを共有するかどうか
  - 共有すると、**GRUB**と呼ばれるメニューのようなものが起動時に毎回開き、windowsとubuntuどっちを起動するかを選ぶみたいな感じになります
  - この場合だと最初に読み込まれるのはSSD固定(ブートローダーがそこなので)
- HDDに独立したESP(TODO:??)をつくる
  - つまりはそれぞれのディスクにブートローダーが入っていて、BIOSからどっちを優先して起動するかを設定してあげるような感じ
  - これだと毎回起動時の確認とかは入らないです

今回は後者を行います

## その前にやること

### 回復ドライブの作成

初めてやるならwindows11側のバックアップをとっておくと安心でしょう  
やり方は他に任せます(https://repair.dospara.co.jp/blog/notes_recoverymedia3 とか)

### Bitlockerの回復キー取得

ブートの構成とかが変わると回復キーを要求されることがあるらしいです

```sh
PS C:\WINDOWS\system32> manage-bde -protectors -get C: 
BitLocker ドライブ暗号化: 構成ツール Version 10.0.26100
Copyright (C) 2013 Microsoft Corporation. All rights reserved.

ボリューム C: [Windows]
すべてのキーの保護機能

エラー: キーの保護機能は見つかりませんでした。


PS C:\WINDOWS\system32> manage-bde -status C:
BitLocker ドライブ暗号化: 構成ツール Version 10.0.26100
Copyright (C) 2013 Microsoft Corporation. All rights reserved.

ボリューム C: [Windows]
[OS ボリューム]

    サイズ:                 930.52 GB
    BitLocker のバージョン: なし
    変換状態:               暗号化は完全に解除されています
    暗号化された割合:       0.0%
    暗号化の方法:           なし
    保護状態:               保護はオフです
    ロック状態:             ロック解除
    識別子フィールド:       なし
    キーの保護機能:         見つかりません
```

私のは暗号化されてませんでした...

