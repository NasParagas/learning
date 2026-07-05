# 基本的な型

- Rustは暗黙的な型変換は行わない
  - i16->i32もしない
  - `num as i32`のように明示的に変換できる

以下二つは全く同じ機械語を生成する
(型推論をしてくれる、ということ)

```rust
    fn build_vector() -> Vec<i16> {
        let mut v: Vec<i16> = Vec::<i16>::new();
        v.push(10i16);
        v
    }
    fn build_vector_2() -> Vec<i16> {
        let mut v = Vec::new();
        v.push(10);
        v
    }
```

型の種類は以下


| 型 | 説明 | 値の例 |
| --- | --- | --- |
| `i8, i16, i32, i64, i128, u8, u16, u32, u64, u128` | 指定されたビット長の符号あり、符号なし整数 | `42`, `-5i8`, `0x400u16`, `0o100i16`, `20_922_789_888_000u64`, `b'*'`（u8のバイトリテラル） |
| `isize, usize` | 計算機のアドレスと同じサイズ（32または64ビット）の符号あり、符号なし整数 | `137`, `-0b0101_0010isize`, `0xffff_fc00usize` |
| `f32, f64` | 単精度もしくは倍精度のIEEE浮動小数点数 | `1.61803`, `3.14f32`, `6.0221e23f64` |
| `bool` | 真偽値 | `true`, `false` |
| `char` | ユニコード文字、32ビット長 | `'*'`, `'\n'`, `'字'`, `'\x7f'`, `'\u{CA0}'` |
| `(char, u8, i32)` | タプル：型が混ざっていてもよい | `('%', 0x7f, -1)` |
| `()` | 「ユニット」（空の）タプル | `()` |
| `struct S { x: f32, y: f32 }` | 名前付きフィールド型構造体 | `S { x: 120.0, y: 209.0 }` |
| `struct T(i32, char);` | タプル型構造体 | `T(120, 'X')` |
| `struct E;` | ユニット型構造体、フィールドを持たない | `E` |
| `enum Attend { OnTime, Late(u32) }` | 列挙型、代数データ型 | `Attend::Late(5)`, `Attend::OnTime` |
| `Box<Attend>` | ボックス：ヒープ上の値へのポインタを保持する | `Box::new(Late(15))` |
| `&i32, &mut i32` | 共有参照と、可変参照：参照先を所有していないので参照先よりも長生きしてはいけない | `&s.y`, `&mut v` |
| `String` | UTF-8文字列。サイズは動的に変化する | `"ラーメン: ramen".to_string()` |
| `&str` | 文字列への参照。UTF-8テキストへの、所有権のない参照 | `"そば: soba"`, `&s[0..12]` |
| `[f64; 4], [u8; 256]` | 固定長配列。要素はすべて同じ型 | `[1.0, 0.0, 0.0, 1.0]`, `[b' '; 256]` |
| `Vec<f64>` | 可変長ベクタ。要素はすべて同じ型 | `vec![0.367, 2.718, 7.389]` |
| `&[u8], &mut [u8]` | スライスへの参照。配列やベクタの一部への参照。ポインタと長さからなる | `&v[10..20]`, `&mut a[..]` |
| `Option<&str>` | オプション値：None（値がない）もしくはSome(v)（値vが存在） | `Some("Dr.")`, `None` |
| `Result<u64, Error>` | 失敗する可能性のある操作の結果。Ok(v)（成功時）もしくはErr(e)（失敗時）。 | `Ok(4096)`, `Err(Error::last_os_error())` |
| `&dyn Any, &mut dyn Read` | トレイトオブジェクト：指定されたメソッドの集合を実装した任意の値への参照。 | `value as &dyn Any`, `&mut file as &mut dyn Read` |
| `fn(&str, usize) -> isize` | 関数へのポインタ | `i32::saturating_add` |
| （クロージャの型は記述する方法がない） | クロージャ | `\|a, b\| a*a + b*b` |


## 固定長数値

### 整数

- 基本は他の言語と同じ。u8は符号なし8bit整数、iは符号あり。  
- 文字と数値は区別される(`char`で数値を表す謎現象は起こらない)  
- `43u8`のように数値型を指定可能。型が指定されない場合、決定できるようになるまで先送りにされるが、整数リテラルの型変数{integer} が型推論の終わりまで未確定だった場合、デフォルトでi32に解決される(`i32`が候補として外れている場合はエラーとなる)  
- `0xff`のように冒頭にn進数のリテラルをつけられる
- `4_421_000`, `0x_fff`のように、数字の任意の間に`_`を入れられる
- `b'A'`==`65_u8`となる。byte literalはASCII文字のみ入れられる

```rust
    // println!("{}", (-4).abs()); ←コンパイルエラー
    println!("{}", (-4_i32).abs());
    println!("{}", i32::abs(-4));
```

上述の通り、数値型が指定されない場合は決定されるのが全てのメソッド呼び出しが解決された上でそれでも型が確定しない場合。なので、ある型固有(ここではint。unsign intに対して`abs()`は実装されていない)のメソッドを解決する際には指定していないとコンパイラが困る  
また、メソッド呼び出しは単項前置演算子よりも優先順位が高いため、

```rust
    println!("{}", -4_i32.abs());
```

のようにすると、`-4`となる

デバッグビルド(普通のcargo build)の場合、整数演算中のオーバーフローは検出されてpanicする

```rust
    let mut i = 1;
    loop {
        i *= 10;
        println!("{}", i);
        std::thread::sleep(Duration::from_secs_f32(0.5));
    }
```

`cargo build --release`の場合は、wrap演算されpanicとはならない  
wrap演算==数学的に正しい答えを、値の範囲で除算した余りを返す  
以下は意図的にwrap演算を用いる例

```rust
    assert_eq!(100_u16.wrapping_mul(200), 20000);
    assert_eq!(500_u16.wrapping_mul(500), 53392);
    assert_eq!(500_i16.wrapping_mul(500), -12144);
```

また、release buildの場合にもpanicさせたい場合は、check付き演算を利用するのが良さそう  
`Option`として返却され、数学的に正しい答えが得られた場合にはその値を`v`として`Some(v)`が、そうでなければ`None`を返す

```rust
    assert_eq!(10_u8.checked_add(20), Some(30));
    assert_eq!(100_u8.checked_add(200), None);
    let x = 100_u8;
    let y = 200_u8;
    // let sum = x.checked_add(y).unwrap(); ←panic
```

そもそもオーバーフローを発生させたくない場合は、飽和演算を用いるのも良さそう

```rust
    assert_eq!(253_u8.saturating_add(10), 255);
```

オーバーフローしていることを判定する演算もある

```rust
    assert_eq!(253_u8.overflowing_add(10), (253_u8.wrapping_add(10), true));
```

### 浮動小数点数

`f32`, `f64`があり、基本的にはC++のfloat, doubleにあたる  
リテラル全部込みにすると`31415.92e-4f64`のようにかける  

```rust
    // 正負の無限大、NAN, MINMAXがある
    assert_eq!(-1. / f32::INFINITY, 0.0);
    assert_eq!(-f32::MIN, f32::MAX);
```

## 真偽値型

```rust
    // bool
    assert_eq!(2 > 5, false);
    // 暗黙的なint等への変換はされない(そもそもコンパイルできない)
    // assert_eq!(1==true, 1)
```

- rustのboolは1byte使う。これにより、bool値に対してポインタを作れるようになっている
  - TODO:作れない言語がある？

```rust
    println!("{}", std::mem::size_of::<bool>());
    println!("{}", std::mem::align_of::<bool>());
    let b = true;
    let p: *const bool = &b;
    println!("address of bool   = {:p}", p);
    let t = true;
    let f = false;
    let tb: u8 = unsafe { std::mem::transmute(t) };
    let fb: u8 = unsafe { std::mem::transmute(f) };
    println!("true  as byte = {}", tb);
    println!("false as byte = {}", fb);
```

## 文字

- 1文字に対しては`char`、文字列やテキストのstreamに対してはUTF-8エンコードを用いる
  - つまり文字列やテキストはUTF-8バイト列として保持される

```rust
    assert_eq!('*' as i32, 42);
```

## tuple

- 型の組み合わせのN個組を表す

```rust
    // "hello"と言う書き方をすると、"コンパイル時にバイナリへ埋め込まれた固定文字列への参照"となり、所有権を持たないため&strとなる...?
    let tuple_exp: (&str, i32, bool) = ("hello", 5, true);
    let txt = "hello world";
    let (head, tail) = txt.split_at(6);
    assert_eq!(head, "hello ");
    assert_eq!(tail, "world");
```

- 配列との違い
  - 配列はすべての要素が同一の方でないといけない
  - tupleは定数のインデックスでのみアクセスできる
    - 各要素のサイズが違うから....とか？
- 「とても単純にかける構造体」と言うイメージも悪くない
- 0要素のtupleを慣用的に**ユニット型**と呼ぶ
  - 意味のある値を渡す必要がないにも関わらず、contextがなんらかの型を要求する場合にユニット型を用いる
  - `save_image(filename: &str) -> Result<(), std::io::Error>`であれば、成功すれば何も返さず、失敗した時には`std::io::Error`がかえる

## ポインタ型

- Rustでは、ある値から別の値を指す場合には必ず明示的にポインタを用いなければならない
  - (TODO: 他言語でそうでない場合の例)
- ポインタ型は未定義動作をしないようにコンパイラが保証してくれるため、C++等よりも扱いは楽

### 参照

- `&String`, `&i32`のように書く
  - `ref string`と読む
  - `&x`を、Rustでは"xへの参照を借用する"という
  - 参照rに対して`*r`とするとrが指す値を取得する
- **null pointer**は存在できない
  - `unsafe`は除く
- 参照には以下の2種類がある
  - `&T`
    - 変更不能な共有参照。複数持つことができる
  - `&mut T`
    - 排他可変参照。この参照がある間が、共有参照も可変参照も作成不可

```rust
    let mut num = 30;
    let mut num2 = 100;
    println!("{}", num);
    let ref_num = &mut num;
    *ref_num = 40;
    // println!("{}", num);  // 可変参照が作られているので`ref_num`経由でしかアクセスできずエラー
    println!("{}", ref_num);
    println!("{}", num); // ここであればこれ以降`ref_num`が使われていないのでok。どこかで使うとまたエラーになる
    let ref2_num = &num;
    println!("{}", num); // 共有参照であれば問題なくアクセスできる
    // ref_num = &mut num2; // ref_numはmutableでないのでエラー
    let mut ref3_num = &mut num;
    println!("{}", ref3_num);
    ref3_num = &mut num2;
    println!("{}", ref3_num);
```

- これらに関するエラーはすべてコンパイル時に見つけてくれる(`rust-analyzer`も見つけてくれる)ので嬉しい！

### Box

- `Box::new`でヒープに値を確保できる
  - ヒープに値を確保することで、**move**されていない限り、変数がスコープから外れるとメモリは即座に解放される
  - (TODO: 他にいいことある？)

```rust
    let t = (12, "eggs");
    let b = Box::new(t);
```

### rawポインタ

- `*mut T`,`*const T`というrawポインタ型がある
- が、`unsafe`を使わなければいけないためここでは割愛

## 配列、vector、slice

- `[T; N]`: 型TのN個の配列を表す。スタック上に確保され、追加・縮小はできない
- `Vec<T>`: 型Tのvector。ヒープ上に確保されるため、要素の追加、他vectorをくっつけたりなどできる
- `&[T]`,`&mut [T]`: 型Tの共有slice、可変slice。配列やvectorの一部の連続した要素への参照
- `v`がこれらの型である場合、`v.len()`は`v`の要素数を表し、`v[i]`は`v`のi番目の要素となる
  - runtimeは`i`が範囲内であるかをチェックし、範囲外にアクセスしようとすればpanicを起こす
- 

