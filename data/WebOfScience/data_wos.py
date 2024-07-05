from transformers import AutoTokenizer
import os
import torch
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import json
from collections import defaultdict
import datasets

np.random.seed(7)

if __name__ == '__main__':
    # tokenizer = AutoTokenizer.from_pretrained('facebook/bart-base')
    label_to_id = {}
    parent_to_children = defaultdict(set)
    data = datasets.load_dataset('json', data_files='wos_total.json')['train']
    for l in data['doc_label']:
        if l[0] not in label_to_id:
            label_to_id[l[0]] = len(label_to_id)
    for l in data['doc_label']:
        assert len(l) == 2
        if l[1] not in label_to_id:
            label_to_id[l[1]] = len(label_to_id)
        parent_to_children[label_to_id[l[0]]].add(label_to_id[l[1]])
    # id_to_label = {i: v for v, i in label_to_id.items()}
    # torch.save(id_to_label, 'id_to_label.pt')
    # torch.save(parent_to_children, 'parent_to_children.pt')
    #改为json方式保存.set无法被序列化
    id_to_label = {i: v for v, i in label_to_id.items()}
    parent_to_children = {i: list(v) for i, v in parent_to_children.items()}
    with open("id_to_label.json",'w',encoding="UTF-8") as wf:
        json.dump(id_to_label,wf,ensure_ascii=False)
    with open("parent_to_children.json", 'w', encoding="UTF-8") as wf:
        json.dump(parent_to_children, wf, ensure_ascii=False)

    id = [i for i in range(len(data))]
    np_data = np.array(id)
    np.random.shuffle(id)
    np_data = np_data[id]
    train, test = train_test_split(np_data, test_size=0.2, random_state=0)
    train, val = train_test_split(train, test_size=0.2, random_state=0)
    train = train.tolist()
    val = val.tolist()
    test = test.tolist()
    with open('WebOfScience_train.json', 'w') as f:
        for i in train:
            line = json.dumps({'token': data[i]['doc_token'], 'label': [label_to_id[i] for i in data[i]['doc_label']]})
            f.write(line + '\n')
    with open('WebOfScience_dev.json', 'w') as f:
        for i in val:
            line = json.dumps({'token': data[i]['doc_token'], 'label': [label_to_id[i] for i in data[i]['doc_label']]})
            f.write(line + '\n')
    with open('WebOfScience_test.json', 'w') as f:
        for i in test:
            line = json.dumps({'token': data[i]['doc_token'], 'label': [label_to_id[i] for i in data[i]['doc_label']]})
            f.write(line + '\n')
