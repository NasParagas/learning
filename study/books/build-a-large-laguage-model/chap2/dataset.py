import torch
from torch.utils.data import Dataset, DataLoader

class GPTDatasetV1(Dataset):
    """
    GPT学習用にtextをsliding windowで分割して作成するDataset
    text全体をtokenizeし、max_length長のinput sequenceとそれを1tokenずらした target sequence の paie を生成
    """
    def __init__(self, txt, tokenizer, max_length, stride):
        self.input_token_ids = []
        self.target_token_ids = []
        token_ids = tokenizer.encode(txt)

        # tokenをmax_lengthの長さのsequenceに分割
        for i in range(0, len(token_ids) - max_length, stride):
