## 未知のバイナリの読み方

### fileコマンド: ファイル形式の特定

file format == 0,1のバイナリの解釈の方法  
`file`コマンドで指定ファイルの情報を確認できる

```sh
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ echo "hello" > hello.txt
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ zip -r hello.zip hello.txt 
  adding: hello.txt (stored 0%)
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ tar -cvf hello.tar hello.txt 
hello.txt
```

```sh
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ file hello.txt 
hello.txt: ASCII text

nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ file hello.zip 
hello.zip: Zip archive data, made by v3.0 UNIX, extract using at least v1.0, last modified Jun 14 2026 16:27:08, uncompressed size 6, method=store

nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ file hello.tar 
hello.tar: POSIX tar archive (GNU)
```

拡張子を消しても確認可能

```sh
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ file data1 
data1: ASCII text
```

### 人力fileコマンド

#### とりあえずバイナリを眺める

2進数だと長いので、16進数でみる

```sh
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ hexdump hello.txt 
0000000 6568 6c6c 0a6f                         
0000006

nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ hexdump --help
 -C, --canonical           canonical hex+ASCII display

nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ hexdump -C data1
00000000  68 65 6c 6c 6f 0a                                 |hello.|
00000006
```

(8bit == 1byte)  
各行の先頭はファイルの先頭から何byte離れた位置にあるか(offset)を表す。ここの値はファイルサイズと一致する

```sh
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ stat data1 
  File: data1
  size: 6               Blocks: 8          IO Block: 4096   regular file
Device: 253,2   Inode: 2625640     Links: 1
Access: (0664/-rw-rw-r--)  Uid: ( 1000/     nas)   Gid: ( 1000/     nas)
Access: 2026-06-14 16:29:05.513260489 +0900
Modify: 2026-06-14 16:29:00.998634607 +0900
Change: 2026-06-14 16:29:00.998634607 +0900
 Birth: 2026-06-14 16:29:00.998275567 +0900
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ du data1 
4       data1
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ du -b data1 
6       data1
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ du -h data1 
4.0K    data1
```

一致してるのかしてないのかわからん...  
`du`, `du -h`の方はディスク上で実際に占有しているブロック数(物理サイズ)を出しているらしい。ファイルシステムはファイルをブロック単位で割り当てる(大体4kbらしい)ため、小さいファイルでも最低1ブロック使う。実際のディスク占有量もこっち  
`du -b`とか`stat`はファイルの論理サイズを出していて、ファイル自体の大きさはちゃんと6byteになってそう  

#### catで見れば良いのでは？

制御文字によって文字の可視性を制御されているかも

```sh
# printf == 引数で渡した文字列を出力してくれる
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ printf "in\b\bvisible\n" > invisible.txt
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ cat invisible.txt 
visible
```

`\b`はBackSpaceに相当する制御文字で、`in`は一瞬表示されるものの`\b`によって消される  
`hexdump`ならそんな細工も問題ない

```sh
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ hexdump -C invisible.txt 
00000000  69 6e 08 08 76 69 73 69  62 6c 65 0a              |in..visible.|
0000000c
```

#### headerに含まれるmagic number

テキストファイル以外の多くのバイナリファイルにはheaderと呼ばれるデータが先頭についている。これはそのバイナリがどのようなデータを表しているものか、解釈する際に必要となるパラメータはどのようなものなのかをOSやapplication伝達するためのもの  

```sh
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted$ hexdump -C $(which ls) | head -n 1
00000000  7f 45 4c 46 02 01 01 00  00 00 00 00 00 00 00 00  |.ELF............|
```

上記は`ls`コマンドの最初の16byte  
ELFという実行ファイルの形式は、"最初の1byteは`0x7f`で、その後に'ELF'の3文字が続く"と使用で定められている  

zipをhexdumpしてみる

```sh
nas@nas-QEMU-Virtual-Machine:~/ws/binary-hacks-rebooted/chap1$ hexdump -C hello.zip 
00000000  50 4b 03 04 0a 00 00 00  00 00 64 83 ce 5c 20 30  |PK........d..\ 0|
00000010  3a 36 06 00 00 00 06 00  00 00 09 00 1c 00 68 65  |:6............he|
00000020  6c 6c 6f 2e 74 78 74 55  54 09 00 03 cb 57 2e 6a  |llo.txtUT....W.j|
00000030  cb 57 2e 6a 75 78 0b 00  01 04 e8 03 00 00 04 e8  |.W.jux..........|
00000040  03 00 00 68 65 6c 6c 6f  0a 50 4b 01 02 1e 03 0a  |...hello.PK.....|
00000050  00 00 00 00 00 64 83 ce  5c 20 30 3a 36 06 00 00  |.....d..\ 0:6...|
00000060  00 06 00 00 00 09 00 18  00 00 00 00 00 01 00 00  |................|
00000070  00 b4 81 00 00 00 00 68  65 6c 6c 6f 2e 74 78 74  |.......hello.txt|
00000080  55 54 05 00 03 cb 57 2e  6a 75 78 0b 00 01 04 e8  |UT....W.jux.....|
00000090  03 00 00 04 e8 03 00 00  50 4b 05 06 00 00 00 00  |........PK......|
000000a0  01 00 01 00 4f 00 00 00  49 00 00 00 00 00        |....O...I.....|
000000ae
```

`PK`という文字列は、zipファイル内部で利用されているデータ構造のヘッダ部分に置かれている値で、zipファイルであることを示す良い手掛かりになる  
各ファイルによって異なってくるので、このような繰り返し出現する特徴的な値をみるだけでも、ファイル形式を知るヒントが得られることがある  
古いtarファイルなど例外もある  
`file`コマンドは"headerに含まれるであろうmagic numberをファイル形式の対応関係をまとめたDBを参照"することによってファイル形式を特定するようになっているが、magic numberをも体内可能性があるファイル形式については判別コードが特別に実装されている(https://github.com/file/file/blob/master/src/is_tar.c)




