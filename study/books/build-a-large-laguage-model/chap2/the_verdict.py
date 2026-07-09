import urllib.request
import os
import re

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

# tokenize
preprocessed = re.split(r'([..:;?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in preprocessed if item.strip()]
# print(len(preprocessed))
# print(preprocessed[:30])

# 重複削除してid付与
all_words = sorted(set(preprocessed))
# print(len(all_words))
vocab = {token: integer for integer, token in enumerate(all_words)}
for i, item in enumerate(vocab.items()):
    # print(item)
    if i >= 50:
        break
print(vocab.items())
