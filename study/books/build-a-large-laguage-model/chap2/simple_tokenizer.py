import os
import urllib.request
import re


class SimpleTokenizerV1:
    def __init__(self, vocab):
        self.token_to_id = vocab
        self.id_to_token = {id: token for token, id in vocab.items()}

    # txetをtoken idへ変換
    def encode(self, text):
        preprocessed = re.split(r'([.,:;?_!"()\']|--|\s)', text)
        # https://docs.python.org/3/library/stdtypes.html#str.strip
        # spaceと空文字削除
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        preprocessed = [item if item in self.token_to_id else "<|unk|>" for item in preprocessed]
        ids = [self.token_to_id[token] for token in preprocessed]
        return ids

    # idからtextへ変換
    def decode(self, ids):
        text = " ".join([self.id_to_token[id] for id in ids])
        # 指定された句読点の前にあるspaceを削除
        text = re.sub(r'\s+([.,?!"()\'])', r"\1", text)
        return text


def main():
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
    preprocessed = re.split(r'([.,:;?_!"()\']|--|\s)', raw_text)
    preprocessed = [item.strip() for item in preprocessed if item.strip()]
    # print(len(preprocessed))
    # print(preprocessed[:30])

    # 重複削除してid付与
    all_tokens = sorted(set(preprocessed))
    all_tokens.extend(["<|endoftext|>", "<|unk|>"])
    vocab = {token: integer for integer, token in enumerate(all_tokens)}
    print(len(vocab.items()))
    tokenizer = SimpleTokenizerV1(vocab)
    text = """"It's the last he painted, you know,"Mrs. Gisburn said with pardonable pride."""
    ids = tokenizer.encode(text)
    print(ids)
    print(tokenizer.decode(ids))

    text1 = "hello world."
    text2 = "good evening."
    text = " <|endoftext|> ".join((text1, text2))
    tokenizer = SimpleTokenizerV1(vocab)
    print(tokenizer.encode(text))
    print(tokenizer.decode(tokenizer.encode(text)))






if __name__ == "__main__":
    main()
