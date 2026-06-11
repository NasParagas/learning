# decisions

様々な決め事を記録する

## git関連の決め事

### repositoryの境界

- 以下の場合はrepositoryを分ける
  - 技術書等の写経
    - このコードは再利用するものではないため
  - ツールチェイン(cargo, uv等)
    - LSPやbuild toolを機能させるため
    - gitignoreを綺麗にするため
    - ただし技術書写経のrepositoryを除く

### commit message

- `add: ~~~`, `#2 fix: ~~~`等とする

## 知識の集約

- `learning/notes`へ

