(vim-commandも含む)  
基本的には`:help`を見ましょう  
[ブラウザ](https://neovim.io/doc/)の方が検索性が良い  

## vim command

### 履歴

いくつか方法ある

- `:`とうって↑
- `:echo` とうって↑で`echo`から始まるものだけ遡れる
- `q:`で履歴を位置欄で遡れる。`j/k enter`で実行も可能

### パス

`%`がカレントディレクトリを起点としたファイルパスを表す

```vim
:echo expand("%")
"notes/neovim/neovim-api.md"
```


現在のファイルの絶対パスを表示

```vim
:echo expand("%:p")
```



