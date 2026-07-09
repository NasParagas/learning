- AndroidはLinuxベースのOS
- IoT分野でのLinuxには`AWS IoT EduKit`が参考になる
  - (気になる)
- RISC-VってARMとかx86とかに並ぶ概念らしい
- 「Rustを使えば、コアライブラリと標準ライブラリだけでbare metal上でどんなアプリも実行できます」
- OSはメモリ管理、割り込み処理、I/Oデバイスとのやりとりなどを行っている。ハードウェアコンポーネントを抽象化し、API(system call)を提供している。高水準プログラミング言語(C,Go, Rust, Pythonなど)はこれらのsyscall上に構築されている
  - 例えばshellにおいては、`id --user`とすることで`getuid`system callが実行される
- Linux Kernel := system callとデバイスドライバの集合
- distribution := Kernel, package管理、ファイルシステムのレイアウト、shellなど、関連要素をまとめたもの
  - [DistroWatch](https://distrowatch.com)に多くのLinux distributionがまとめられている

### リソースの可視化


(コンテナについての正しい認識を持つようにするための言及)  

inuxでは、デフォルトでは全てのプロセスにシステムの全リソースを見れるようにしている(ユーザーに対してはそうではない...はず)
 ここでのリソースとは？

- CPU, RAM, ファイルなどのハードウェアとそれを抽象化したもの
- ファイルシステム
- HDD
- SSD
- プロセス
- ネットワークデバイスやルーティングテーブルなどのネットワーク関連
- credentialなuser情報(username, password)
- など

リソースを見る具体例

```sh
# global(hostOS)のproperty(Linuxのversion)を確認
cat /proc/version
> Linux version 7.0.0-22-generic (buildd@bos03-arm64-083) (aarch64-linux-gnu-gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0, GNU ld (GNU Binutils for Ubuntu) 2.46) #22-Ubuntu SMP PREEMPT_DYNAMIC Mon May 25 15:37:49 UTC 2026

# 使用中のCPU情報
cat /proc/cpuinfo

# 現在のshellのプロセスIDを表示し、プロセス情報を確認($$ == 現在のプロセスを参照する変数)
echo $$
> 20385

cat /proc/$$/status | head -n6
Name:   bash
Umask:  0002
State:  S (sleeping)
Tgid:   20385
Ngid:   0
Pid:    20385

# こんなファイル/フォルダ群がある
nas@nas-QEMU-Virtual-Machine:~/ws/learning-modern-linux$ cat /proc/$$/
attr/              cgroup             comm               environ            fdinfo/            ksm_merging_pages  limits             maps               mounts             ns/                oom_score          patch_state        root/              sessionid          smaps_rollup       statm              task/              timerslack_ns      
autogroup          clear_refs         coredump_filter    exe                gid_map            ksm_stat           loginuid           mem                mountstats         numa_maps          oom_score_adj      personality        sched              setgroups          stack              status             timens_offsets     uid_map            
auxv               cmdline            cwd/               fd/                io                 latency            map_files/         mountinfo          net/               oom_adj            pagemap            projid_map         schedstat          smaps              stat               syscall            timers             wchan              
```

同じPIDは複数存在できる？← namespaceが異なれば存在可能で、Dockerなどのコンテナ化された環境で起こりえる  

### リソースの分離

あるプロセスのメモリ消費が他のプロセスに影響しないように、メモリ使用量を制限し、制限量以上使うとOOMKiller(out-of-memory killer)により強制終了される  
このようなリソース分離にはcgroupというカーネルの機能を使用する(あとで詳しくやる)

### その他

POSIX == UNIX系OSのサービスインターフェースを定義するIEEE規格
