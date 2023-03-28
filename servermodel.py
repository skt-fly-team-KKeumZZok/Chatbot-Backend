import torch
import torch.nn as nn
import random

from model.classifier import KoBERTforSequenceClassfication
from kobert_transformers import get_tokenizer
from model.big import dic
from util.change import Emotion



def load_wellness_answer():
    root_path = "."
    category_path = f"{root_path}/data/wellness_dialog_category.txt"
    answer_path = f"{root_path}/data/wellness_dialog_answer.txt"

    c_f = open(category_path, 'r',encoding='UTF8')
    a_f = open(answer_path, 'r',encoding='UTF8')

    category_lines = c_f.readlines()
    answer_lines = a_f.readlines()

    category = {}
    answer = {}
    for line_num, line_data in enumerate(category_lines):
        data = line_data.split('    ')
        category[data[1][:-1]] = data[0]

    for line_num, line_data in enumerate(answer_lines):
        data = line_data.split('    ')
        keys = answer.keys()
        if (data[0] in keys):
            answer[data[0]] += [data[1][:-1]]
        else:
            answer[data[0]] = [data[1][:-1]]

    return category, answer


def kobert_input(tokenizer, str, device=None, max_seq_len=512):
    index_of_words = tokenizer.encode(str)
    token_type_ids = [0] * len(index_of_words)
    attention_mask = [1] * len(index_of_words)

    # Padding Length
    padding_length = max_seq_len - len(index_of_words)

    # Zero Padding
    index_of_words += [0] * padding_length
    token_type_ids += [0] * padding_length
    attention_mask += [0] * padding_length

    data = {
        'input_ids': torch.tensor([index_of_words]).to(device),
        'token_type_ids': torch.tensor([token_type_ids]).to(device),
        'attention_mask': torch.tensor([attention_mask]).to(device),
    }
    return data

def modeling (user_chat):
    big_cate=set()
    root_path = "."
    checkpoint_path = f"{root_path}/checkpoint"
    save_ckpt_path = f"{checkpoint_path}/past.pth"

    # 답변과 카테고리 불러오기
    category, answer = load_wellness_answer()

    ctx = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(ctx)

    # 저장한 Checkpoint 불러오기
    checkpoint = torch.load(save_ckpt_path, map_location=device)

    model = KoBERTforSequenceClassfication()
    model.load_state_dict(checkpoint['model_state_dict'],strict=False)

    model.to(ctx)
    model.eval()

    tokenizer = get_tokenizer()

    for i in user_chat:
        sent = i  
        data = kobert_input(tokenizer, sent, device, 512)

        output = model(**data)

        logit = output[0]
        softmax_logit = torch.softmax(logit, dim=-1)
        softmax_logit = softmax_logit.squeeze()

        max_index = torch.argmax(softmax_logit).item()
        max_index_value = softmax_logit[torch.argmax(softmax_logit)].item()
        
        hi=dic()
        if str(max_index) in hi:
            michin=hi[str(max_index)]     
        
        #label=category[str(max_index)]
        #label=label.split('/')
        #label1=label[1]
        
        result =Emotion().to_num(michin)
        
        
        big_cate.add(str(result))
        big_cate1=list(big_cate)
        
        temp= ",".join(big_cate1)
        
        
    return(temp)

