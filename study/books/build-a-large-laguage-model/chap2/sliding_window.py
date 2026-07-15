import tiktoken
import os
import urllib.request

# txtのdownload
if not os.path.exists("./the-verdict.txt"):
    url = (
        "https://raw.githubusercontent.com/rasbt/"
        "LLMs-from-scratch/main/ch02/01_main-chapter-code/"
        "the-verdict.txt"
    )
    file_path = "the-verdict.txt"
    urllib.request.urlretrieve(url, file_path)

# 読み込み
with open("./the-verdict.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()
tokenizer = tiktoken.get_encoding("gpt2")

# encode
enc_text = tokenizer.encode(raw_text)
print(len(enc_text))

# 最初の50個のtokenを削除(なんかするらしい)
enc_sample = enc_text[50:]

# 入力変数と目的変数のpairの作成
context_size = 4
for i in range(1, context_size+1):
    context = enc_sample[:i]
    desired = enc_sample[i]
    # 入力変数 ---> 目的変数
    print(context, "--->", desired)

