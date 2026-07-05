## commit操作

### 取り消し

```sh
git reset --soft HEAD^
```

### 

## remote repositoryとの紐付け

```sh
git remote
```

とすると、local repoに登録されているremote repoの名前一覧を表示できる  

```sh
git remote -v
git remote show origin
```

等とすればもっと細かい情報も見れる。基本的には、`origin`という名前が表示されるはず
この`origin`というのはあくまでAlias的なものなので、自由に変更可能。実体はURL  
`git clone`をする場合に、最初のremote repoのURLが`origin`となる

```sh
git remote -v
# origin  https://github.com/NasParagas/learning.git (fetch)
```


```sh
git remote --help
       rename
           Rename the remote named <old> to <new>. All remote-tracking branches and configuration settings for the remote are
           updated.

           In case <old> and <new> are the same, and <old> is a file under $GIT_DIR/remotes or $GIT_DIR/branches, the remote is
           converted to the configuration file format.
```

```sh
git remote rename origin nas
git remote -v
# nas     https://github.com/NasParagas/learning.git (fetch)
```

`git clone`ではなく、既にlocalに存在するrepoをremoteと紐づける際は`git remote add`を使う

```sh
git remote add <name> <url>
```

`git remote -v`で見たように、URLを`<name>`に紐づけている。 `<name>`には前述した`origin`に当たるものをいれる
紐付け後は、remoteのmain branchと紐づけるためのlocalのbranchを作成する必要がある。`git commit`等をすれば勝手に作られる  

```sh
git add .gitignore
git commit -m "add: gitignore"
git branch  # main
```

branch作成後、(`LICENSE`を持ってくるために)`git pull`を行う。この時に、remoteのmain(origin/main)をlocalのどのbranchに紐づけるかを設定する必要がある  

```sh
git branch --set-upstream-to=origin/main main
git pull

hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint:
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint:
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
```

あれ  
`fatal: Need to specify how to reconcile divergent branches.`
とのことで、履歴の大元が一緒じゃないのでどうすれば良いのでしょうかという感じ  
それぞれの説明はclaudeちゃんのやつがわかりやすかったので転記

```txt
  1. pull.rebase false（merge / マージ）

  リモートの変更を取り込み、マージコミットを1つ作って2つの履歴を合流させます。

    A---B---C  (ローカル)
   /
  O
   \
    D---E      (リモート)

           ↓ pull (merge)

    A---B---C---M  (M = マージコミット)
   /           /
  O           /
   \         /
    D---E---/

  - 元の履歴がそのまま残る（安全・改変しない）
  - マージコミットが増えて履歴が枝分かれして見える

  2. pull.rebase true（rebase / リベース）                                         
                                                                                   
  自分のコミットを一旦どけて、リモートの先端に付け替え直します。履歴が一直線になり 
  ます。                                                                           
                                                                                   
    A---B---C   (ローカル)                                                         
   /                                                                               
  O                                                                                
   \                                                                               
    D---E       (リモート)                                                         
                                                                                   
           ↓ pull --rebase                                                         
                                                                                   
  O---D---E---A'---B'---C'   (一直線)                                              
                                                                                   
  - 履歴がきれいな一直線になる                                                     
  - コミットのハッシュが変わる（A→A'）。push済みのコミットには使わない方が無難     
                                                                                   
  3. pull.ff only（fast-forward only / 早送りのみ）                                
                                                                                   
  ローカルに独自のコミットが無く、ただリモートが先に進んでいるだけのときだけ取り込 
  みます。履歴が分かれている場合は何もせずエラーで止まる。                         
                                                                                   
  - 勝手にマージやリベースをしないので一番安全・予測しやすい                       
  - 履歴が分かれていると失敗する（→自分で merge か rebase を選ぶ）
```

今回の場合はremoteがLICENSEの追加、localがgitignoreの追加で、衝突の余地がないし数も少ないので1,2のどちらでも大丈夫です(3はそもそもできない)  
自分はあんまりrebase好きじゃないのでmergeします  

```sh
git pull origin main --allow-unrelated-histories --no-rebase
```
```sh
git push
```

## repositoryの融合

```sh
cd repo-B  # 統合先のリポジトリ

# リモートとして追加
git remote add <name> <url-or-path>
git fetch <name>

# サブディレクトリとして取り込む(履歴も一緒に)
git subtree add --prefix=repo-a-subdir repo-a-remote main
```

