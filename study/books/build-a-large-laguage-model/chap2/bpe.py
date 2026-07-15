from importlib.metadata import version
import tiktoken

# 50256が`endoftext`のtokenで、BPE tokenizerの語彙の合計サイズも56257
text1 = "hello world."
text2 = "good evening."
text = " <|endoftext|> ".join((text1, text2))
tokenizer = tiktoken.get_encoding("gpt2")
token_ids = tokenizer.encode(text, allowed_special={"<|endoftext|>"})
print(token_ids)

# 未知の単語もtokenizeできる
# その際は、より小さなwordとするか、バラバラの文字に分解される
text = "Akwirw ier"
token_ids = tokenizer.encode(text)
print(token_ids)
sentence = tokenizer.decode(token_ids)
print(sentence)



