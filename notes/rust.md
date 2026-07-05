# Rust

## Rustとは？
TODO:概要らしい概要

### CやC++などの、他のシステムプログラミングのための言語との違い

#### 未定義動作

- CやC++では、ゼロ除算やオーバーフローなどの未定義動作をコンパイラが検出してくれるわけではなく、それらを避ける責任は全てプログラマーにある
- 未定義動作はセキュリティ上の欠陥となりうる(アクセスすべきでない要素にアクセスしてしまった結果、呼ばれるはずのない関数を呼んでしまったり)
  - モリスワームとか
- Rustでは、コンパイルが通った場合、未定義動作が存在しないことを保証する
  - バグがなくなるわけではない
  - TODO: バグの例

#### 並列プログラミング

- TODO: ちゃんと勉強してからもう一回書き直す
- C,C++で並列プログラミングを行う場合、排他アクセス制御などは自分で行う必要があり、バグのないプログラムにする労力が大きい
- Rustでは、アクセスの競合などをコンパイラが検出してくれるため、格段に並列プログラミングがかきやすくなる


## 環境構築

### `rustup`によるinstall, update

- https://rust-lang.org/ja/tools/install/ に記載のコマンドを実行
- 確認

```sh
cargo --version
>> cargo 1.95.0 (f2d3ce0bd 2026-03-21)
rustc --version
>> rustc 1.95.0 (59807616e 2026-04-14)
rustdoc --version
>> rustdoc 1.95.0 (59807616e 2026-04-14)
```
  - `cargo`: コンパイルマネージャー兼パッケージマネージャー。プロジェクトの作成もビルドも依存ライブラリの管理も行う
  - `rustc`: コンパイラ。`cargo`が起動する(ちょくせつきどうもできる)
  - `rustdoc`: ドキュメンテーションツール。同上
- 以下でupdate

```sh
# stableへのupdate
rustup update stable
# nightly
TODO

# rustup自体のupdate
rustup self update
```

### dockerでの環境構築

```dockerfile
FROM ubuntu:24.04
RUN apt update && apt install -y curl build-essential
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | \
    sh -s -- -y --default-toolchain stable
ENV PATH="/root/.cargo/bin:${PATH}"
CMD ["/bin/bash"]
```

### rustcを使ったbuild、実行

```rust
// ~/Projects/hello_world/main.rs
fn main() {
    println!("Hello, world!");
}
```

```bash
# ~/Projects/hello_world
rustc main.rs
main
# >> Hello, World!
```

### cargoを使ったpackageの作成、buildと実行

```bash
# ~/Projects
cargo new hello
cd hello
```

- `Cargo.toml`にはプロジェクトの名前、バージョン、使用するRustのエディションが記載される
  - `name`の部分が実行ファイルの名前にもなる
  - dependencies以下にはプロジェクトが依存するクレート(パッケージ)を追記していく

```toml
[package]
name = "hello"
version = "0.1.0"
edition = "2024"

[dependencies]
```

```bash
cargo build
```

- 実行ファイルは`./target/debug/hello`
- 生成される`Cargo.lock`にはプロジェクト内の依存関係のバージョン情報が記録されている
- `cargo run`でビルド＆実行
- `cargo check`でコンパイル可能か確認できる
- `cargo build --release`で最適化された状態の実行ファイルをコンパイルできる。この時の実行ファイルは`./target/release/hello`
  - 実行ファイルの実行速度が上がるが、コンパイルに時間がかかる
- `cargo clean`でビルドしたファイルを消せる
- `cargo help <コマンド名>`でコマンドの詳細を確認できる

### cargo.tomlにcrateを追加

- [dependencies]以下に`rand = "0.8.3"`などと記入する
  - 実際には`"^0.8.3"`の省略だが、互換性のためにより上位のバージョンがある場合でも`0.8.3~0.9.0未満`のバージョンが選ばれる
- これを記載して`cargo build`を行ったとき、build時に必要なライブラリがコンパイルされ、`cargo.lock`にクレートのライブラリなどの正確なバージョン関係が追記される
  - `0.9.0`と記載してから再度buildを行うと、その新しいバージョンに従って必要なライブラリのバージョンなども自動で合わせてくれる
  - コードの中では`use rand:Rng`のように使う
    - `rand`: クレート
    - `Rng`: トレイト
    - `thread_rng()`: 関数
    - `gen_range()`: メソッド
    - `cargo run`でクレートの説明の`html`が生成される
      - 本来は`--open`でそのまま開いてくれるが、wslはダメみたい

## 関数・テストの書き方

```rust
fn main() {
    let ans = gcd(67892, 67896);
    println!("{}", ans);
}

// n: u64のようにすることで各仮引数の型を定義、-> u64で返り値の型を定義する
fn gcd(mut n: u64, mut m: u64) -> u64 {
    // falseの場合はpanicする
    assert!(n != 0 && m != 0);
    while m != 0 {
        if m < n {
            // 明示的な場合は以下のように型は省略できる
            let t = m;
            m = n;
            n = t;
        }
        m = m % n;
    }
    // セミコロンなしの式で終わった場合、それが関数の返り値となる。returnは主に早期リターンで用いる
    n
}

#[test]
fn test_gcd() {
    assert_eq!(gcd(14, 15), 1);
    assert_eq!(gcd(2 * 3 * 11 * 19, 2 * 11 * 13 * 23), 2 * 11);
}
```

- `cargo run`で実行、`cargo test`でテストの実行ができる
  - 通常コンパイル時はtestはコンパイルされない
  - TODO: 末尾ではなくファイルを分けることもできるはず

## 型

### ユニット型

[参考](https://doc.rust-lang.org/std/primitive.unit.html)

- 空のタプル(スカラー型)
- 返り値が何もないことを表す
- 「ほかに意味のある値を返せないときに使う」
  - 例えばmain関数はユニット型のユニットを返す？
  - 値であり型でもある
  - `nullptr`で参照解決できちゃうのはおかしいでしょうという前提
- 例えば以下のように返り値として使うこともできる(もちろん省略できる)

```rust
fn hello() -> () {
    println!("hello");
}

fn main() -> () {
    hello();
}
```

- こんなこともできる(ユニット型に代入できるのはユニットのみ)

```rust
    let mut a: Vec<()> = vec![];
    a.push(());

    let b :() = ();
```

### 配列

- 初期化

```rust
let array1 = [1,2,3,4,5];
let array2 = ["monnnitiha"; 10]
```

- 長さはコンパイル時に決定される
- 初期化されていない配列は宣言できない

### ベクタ

- 使用例

```rust
    // ベクタ
    // 初期化
    let mut primes = vec![2,3,5,7];
    let mut vec1 = vec![0; 3];
    let mut pal = Vec::new();

    // collectメソッドを使用した初期化
    let languages: Vec<String> = std::env::args().skip(1).collect();
    for l in languages
    {
        println!("{}: {}",
            l, 
            if l.len() % 2 == 0 { "functional" }
            else { "imperative" }
        );
    }


    // メソッド使用例
    // push
    primes.push(11);
    primes.push(13);
    assert_eq!(primes.iter().product::<i32>(), 30030);

    assert_eq!(vec1, [0,0,0]);

    // pop
    pal.push("step");
    pal.push("on");
    assert_eq!(pal, ["step","on"]);
    pal.pop();
    assert_eq!(pal, ["step"]);

    // capasity
    let mut v = Vec::with_capacity(1);
    assert_eq!(v.capacity(), 1);
    v.push(1);
    v.push(2);
    assert_eq!(v.len(), 2);
    println!("{}", v.capacity());  // 4 (2 -> 4 -> 8 -> 16...)

    // insert
    use quanta;
    vec1.insert(1, 1);
    assert_eq!(vec1, [0,1,0,0]);
    let clock = quanta::Clock::new();
    let mut vec2 = vec![0;1_000_000_000];
    let start = quanta::Instant::now();
    vec2.insert(0, 0);
    let stop = quanta::Instant::now();
    println!("{:?}", stop.duration_since(start));  // 0.25s程度
    let start = quanta::Instant::now();
    vec2.insert(900_000_000, 0);
    let stop = quanta::Instant::now();
    println!("{:?}", stop.duration_since(start));  // 0.015s程度
```

- 動的にサイズ変更が可能(ヒープ上に確保される)
- 以下の三つの値で構成される
  - ヒープ上に確保されるバッファ
    - バッファに達しているときに新たな要素を追加しようとすると、より大きなバッファが確保され、要素がコピーされ、ベクタのポインタと容量が更新されて新しいバッファを刺すようになり、古いバッファが解放される
  - バッファに保持できる容量
  - 現在保持している要素数
  - vec!とVec::new()は何が違う？
    - Vec::with_capacity()というものがあり、vec!はそれを使っている
      - あらかじめ必要な要素数がわかっているとき、バッファの再確保をしないようにするために用いる
      - コンパイル時に要素数を判断してる？

### スライス

- スライスは任意の長さでありうるので、直接変数に格納したり関数の引数として渡すことはできない（つまりつねに参照として渡される）
  - ？
  - 大きさが決まらないから静的に(コンパイル時に)スライスとしては決定できないってこと？
- スライスの参照はファットポインタ(スライスの最初の要素を示すポインタとスライスに含まれる要素数)

```rust
    // 宣言方法(明示的にすることはあまりないと思うけど)
    let v = vec![0.1, 0.2, 0.3];
    let a =     [0.1, 0.2, 0.3];
    let sv: &[f64] = &v;
    let sa: &[f64] = &a;
```

- 上の例では、ベクタ、配列ともにスライスの参照へと変換している
- つまり、ベクタや配列で使いたいメソッドにおいて、スライスへの参照を引数として取るようにすれば、どちらでも使用可能になる

```rust
    fn print_elem(n: &[f64]) -> ()
    {
        for elem in n 
        {
            println!("{}", elem);
        }
    }
    // どっちでも使える
    print_elem(sv);
    print_elem(sa);
    print_elem(&sv[0..1]);
    print_elem(&sa[1..]);
```

- 実際に、`len()`や`sort()`などもスライス型[T]の参照に対するメソッドとして定義されている

![alt text](<../_ATTACHMENT/IMG_7596 2.jpg>)

### Result型

- 

### その他

- 列挙型=enum
  - とりうる値として決まった数の列挙子(variant)を持つ
- `except`メソッドはその

## トレイト

- 型が実装できるメソッドの集合
- 例えば

```rust
use std::str::FromStr;
```
は標準ライブラリのトレイト`FromStr`をスコープの取り込んでいて、`FromStr`トレイトを実装してある型は、このトレイトを使うことができる

## 所有権と移動(move)

- Rustでは、値の直接の所有者(変数)は一つだけ
  - その変数が宣言されたブロックから、プログラムの実行の制御が離れたとき、変数・値とものドロップする
  - 他の変数からその値にコピーせずにアクセスしたい場合、その値を参照するか、所有権を移すことになる
  - 所有権が移った場合、元の所有者は未初期化状態となる
- 所有権を移す == ヒープに保存されている値はそのままに、ポインタ元を変える
- 所有権が移ったことによるコンパイルエラーの例

```rust
fn main() {
    let s = vec!["udon".to_string(), "soba".to_string(), "ramen".to_string()];
    let t = s;
    let u = s;
}

// error[E0382]: use of moved value: `s`
//  --> src/main.rs:5:13
//   |
// 3 |     let s = vec!["udon".to_string(), "soba".to_string(), "ramen".to_string()];
//   |         - move occurs because `s` has type `Vec<String>`, which does not implement the `Copy` trait
// 4 |     let t = s;
//  |             - value moved here
// 5 |     let u = s;
//   |             ^ value used here after move
//   |

```


- 次のような、片方のパスしか通らないようになっている場合には、ちゃんとそこまではコンパイルが通る。その後に移動させようとすると無理

```rust
    let v = vec![1,2];
    if v[0] > v[1]
    {
        mymove(v);
    }
    else
    {
        mymove(v);
    }
    mymove(v);

fn mymove(v: Vec<i32>)
{
   let v2 = v;
}
// error[E0382]: use of moved value: `v`
//   --> src/main.rs:21:12
//    |
// 12 |     let v = vec![1,2];
//    |         - move occurs because `v` has type `Vec<i32>`, which does not implement the `Copy` trait
// ...
// 15 |         mymove(v);
//    |                - value moved here
// ...
// 19 |         mymove(v);
//    |                - value moved here
// 20 |     }
// 21 |     mymove(v);
//    |            ^ value used here after move

```

- 所有権を移動せず、ヒープの値まで複製したい場合は`.clone`を使う

```rust
    let v = vec![1,2];
    let mut v2 = v.clone();
    v2[1] = 1;
    for vi in v
    {
        println!("{}", vi);
    }
    for vi in v2
    {
        println!("{}", vi);
    }

// 1
// 2
// 1
// 1
```

- 基本型の一部には`Copy型`と呼ばれる、上述したような所有権を移動するような操作をした場合に、所有権が移動するのではなく値がコピーされる型がある
  - ディープコピーが負担とならない型、ドロップの際に特別なことをしない型、ヒープを指していない型など？
  - 具体的には`int`, `float`, `bool`など

```rs
    let i = 1;
    let i2 = i;
    let i3 = i;
```

- ユーザー定義型では、すべてのフィールドにCopy型である場合に限り、明示的に属性をつけてあげることでCopy型にすることができる

```rs
// 何もつけない場合
int main()
{
    let l = Label {number:3};
    print(l);
    println!("hello! {}", l.number);
}

struct Label { number: i64}

fn print(l: Label) { println!("Hello {}", l.number)}
// error[E0382]: borrow of moved value: `l`
//   --> src/main.rs:41:27
//    |
// 39 |     let l = Label {number:3};
//    |         - move occurs because `l` has type `Label`, which does not implement the `Copy` trait
// 40 |     print(l);
//    |           - value moved here
// 41 |     println!("hello! {}", l.number);
//    |                           ^^^^^^^^ value borrowed here after move
```

```rs
// 属性をつける
int main()
{
    let l = Label {number:3};
    print(l);
    println!("hello! {}", l.number);
}

#[derive(Clone, Copy)]
struct Label { number: i64}

fn print(l: Label) { println!("Hello {}", l.number)}
// ok
```

```rs
// Copy型でないフィールドがある場合には無理
#[derive(Clone, Copy)]
struct StringLabel { name: String}

// error[E0204]: the trait `Copy` cannot be implemented for this type
//   --> src/main.rs:44:17
//    |
// 44 | #[derive(Clone, Copy)]
//    |                 ^^^^
// 45 | struct StringLabel { name: String}
//    |                      ------------ this field does not implement `Copy`
```

## formatter

- {} とかの
- {}: デフォルト. `std::fmt::Display`で実装される
- {:?}: debug用. `std::fmt::Debug`で実装される
- {:#?}: debug用のフォーマットを改行やインデントでみやすく

## メソッド
### `unwrap()`
- 値があると思われる という前提でその中身を取り出すためのメソッド
- 値がなかった場合はpanicする
- `Option`型に対しては、例えば以下のように使う

```rs
// 値が存在する場合は取得
let x = Some(10);
let n = x.unwrap();
println!("{}", n);  // 10

// 値がない場合はpanic
let x: Option<i32> = None;
let n = x.upwrap();  // panic
```

- 

## `unsafe`
- コンパイラに安全性の保証をさせない区画

## pub

```

pub              // どこからでも見える
pub(crate)       // 同じ crate 内なら見える
pub(super)       // 親モジュールまで見える
pub(in path)     // 指定したモジュール範囲だけ見える
```
