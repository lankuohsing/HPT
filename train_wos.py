import random
import json
from transformers import AutoTokenizer
import torch
from torch.utils.data import Subset, DataLoader
from torch.optim import Adam
import torch.nn as nn
import os
import datasets
from tqdm import tqdm
import argparse
import wandb

from eval import evaluate

import utils


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lr', type=float, default=3e-5)
    parser.add_argument('--data', type=str, default='WebOfScience')
    parser.add_argument('--batch', type=int, default=4)
    parser.add_argument('--early-stop', type=int, default=6)
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--name', type=str, default='test')
    parser.add_argument('--update', type=int, default=1)
    parser.add_argument('--model', type=str, default='prompt')
    parser.add_argument('--wandb', default=False, action='store_true')
    parser.add_argument('--arch', type=str, default='/Users/guoxing.lan/projects/models/bert-base-uncased')
    parser.add_argument('--layer', type=int, default=1)
    parser.add_argument('--graph', type=str, default='GAT')
    parser.add_argument('--low-res', default=False, action='store_true')
    parser.add_argument('--seed', default=3, type=int)
    return parser


class Save:
    def __init__(self, model, optimizer, scheduler, args):
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.args = args

    def __call__(self, score, best_score, name):
        torch.save({'param': self.model.state_dict(),
                    'optim': self.optimizer.state_dict(),
                    'sche': self.scheduler.state_dict() if self.scheduler is not None else None,
                    'score': score, 'args': self.args,
                    'best_score': best_score},
                   name)


if __name__ == '__main__':
    parser = parse()
    args = parser.parse_args()
    if args.wandb:
        wandb.init(config=args, project='HPT')
    print(args)
    utils.seed_torch(args.seed)

    tokenizer = AutoTokenizer.from_pretrained(args.arch)
    data_path = os.path.join('data', args.data)
    args.name = args.data + '-' + args.name
    batch_size = args.batch

    #{int: str}
    id_to_label = torch.load(os.path.join(data_path, 'value_dict.pt'))
    # with open(os.path.join(data_path, 'id_to_label.json'),'r',encoding="UTF-8") as rf:
    #     id_to_label=json.load(rf)
    # id_to_label = {int(i): v for i, v in id_to_label.items()}
    #{int: set(int)}
    parent_to_children = torch.load(os.path.join(data_path, 'slot.pt'))
    # with open(os.path.join(data_path, 'parent_to_children.json'),'r',encoding="UTF-8") as rf:
    #     parent_to_children=json.load(rf)
    # parent_to_children = {int(i): v for i, v in parent_to_children.items()}
    child_to_parent = {}
    num_class = 0
    for s in parent_to_children:
        for v in parent_to_children[s]:#set和list都可以for 循环遍历
            child_to_parent[v] = s
            if num_class < v:
                num_class = v
    num_class += 1
    path_list = [(i, v) for v, i in child_to_parent.items()]
    for i in range(num_class):
        if i not in child_to_parent:
            child_to_parent[i] = -1#第一层的标签是没有父节点的


    def get_depth(x):
        depth = 0
        while child_to_parent[x] != -1:
            depth += 1
            x = child_to_parent[x]
        return depth


    id_to_depth = {i: get_depth(i) for i in range(num_class)}
    max_depth = id_to_depth[max(id_to_depth, key=id_to_depth.get)] + 1
    depth_to_id = {i: [a for a in id_to_depth if id_to_depth[a] == i] for i in range(max_depth)}

    for depth in depth_to_id:
        for l in depth_to_id[depth]:
            path_list.append((num_class + depth, l))

    if args.model == 'prompt':
        if os.path.exists(os.path.join(data_path, args.model)):
            dataset = datasets.load_from_disk(os.path.join(data_path, args.model))
        else:
            dataset = datasets.load_dataset('json',
                                            data_files={'train': 'data/{}/{}_train.json'.format(args.data, args.data),
                                                        'dev': 'data/{}/{}_dev.json'.format(args.data, args.data),
                                                        'test': 'data/{}/{}_test.json'.format(args.data, args.data), })

            prefix = []
            for i in range(max_depth):
                prefix.append(tokenizer.vocab_size + num_class + i)
                prefix.append(tokenizer.vocab_size + num_class + max_depth)
            prefix.append(tokenizer.sep_token_id)


            def data_map_function(batch, tokenizer):
                new_batch = {'input_ids': [], 'token_type_ids': [], 'attention_mask': [], 'labels': []}
                for l, t in zip(batch['label'], batch['token']):
                    new_batch['labels'].append([[-100 for _ in range(num_class)] for _ in range(max_depth)])
                    for d in range(max_depth):
                        for i in depth_to_id[d]:
                            new_batch['labels'][-1][d][i] = 0
                        for i in l:
                            if new_batch['labels'][-1][d][i] == 0:
                                new_batch['labels'][-1][d][i] = 1
                    new_batch['labels'][-1] = [x for y in new_batch['labels'][-1] for x in y]

                    tokens = tokenizer(t, truncation=True)
                    new_batch['input_ids'].append(tokens['input_ids'][:-1][:512 - len(prefix)] + prefix)
                    new_batch['input_ids'][-1].extend(
                        [tokenizer.pad_token_id] * (512 - len(new_batch['input_ids'][-1])))
                    new_batch['attention_mask'].append(
                        tokens['attention_mask'][:-1][:512 - len(prefix)] + [1] * len(prefix))
                    new_batch['attention_mask'][-1].extend([0] * (512 - len(new_batch['attention_mask'][-1])))
                    new_batch['token_type_ids'].append([0] * 512)

                return new_batch


            dataset = dataset.map(lambda x: data_map_function(x, tokenizer), batched=True)
            dataset.save_to_disk(os.path.join(data_path, args.model))
        dataset['train'].set_format('torch', columns=['attention_mask', 'input_ids', 'labels'])
        dataset['dev'].set_format('torch', columns=['attention_mask', 'input_ids', 'labels'])
        dataset['test'].set_format('torch', columns=['attention_mask', 'input_ids', 'labels'])

        from models.prompt import Prompt

    else:
        raise NotImplementedError
    if args.low_res:
        if os.path.exists(os.path.join(data_path, 'low.json')):
            index = json.load(open(os.path.join(data_path, 'low.json'), 'r'))
        else:
            index = [i for i in range(len(dataset['train']))]
            random.shuffle(index)
            json.dump(index, open(os.path.join(data_path, 'low.json'), 'w'))
        dataset['train'] = dataset['train'].select(index[len(index) // 5:len(index) // 10 * 3])
    model = Prompt.from_pretrained(args.arch, num_labels=len(id_to_label), path_list=path_list, layer=args.layer,
                                   graph_type=args.graph, data_path=data_path, depth2label=depth_to_id, )
    model.init_embedding()

    model.to('cpu')
    if args.wandb:
        wandb.watch(model)

    train = DataLoader(dataset['train'], batch_size=batch_size, shuffle=True, )
    dev = DataLoader(dataset['dev'], batch_size=8, shuffle=False)
    model.to('cpu')
    optimizer = Adam(model.parameters(), lr=args.lr)

    save = Save(model, optimizer, None, args)
    best_score_macro = 0
    best_score_micro = 0
    early_stop_count = 0
    update_step = 0
    loss = 0
    os.makedirs(os.path.join('checkpoints', args.name),exist_ok=True)

    for epoch in range(4):
        if early_stop_count >= args.early_stop:
            print("Early stop!")
            break

        model.train()
        with tqdm(train) as p_bar:
            for batch in p_bar:
                batch = {k: v.to('cpu') if isinstance(v, torch.Tensor) else v for k, v in batch.items()}
                output = model(**batch)
                output['loss'].backward()
                loss += output['loss'].item()
                update_step += 1
                if update_step % args.update == 0:
                    if args.wandb:
                        wandb.log({'loss': loss, })
                    p_bar.set_description(
                        'loss:{:.4f}'.format(loss, ))
                    optimizer.step()
                    optimizer.zero_grad()
                    loss = 0
                    update_step = 0
                    # torch.cuda.empty_cache()

        model.eval()
        pred = []
        gold = []
        with torch.no_grad(), tqdm(dev) as pbar:
            for batch in pbar:
                batch = {k: v.to('cpu') if isinstance(v, torch.Tensor) else v for k, v in batch.items()}
                output_ids, logits = model.generate(batch['input_ids'], depth2label=depth_to_id, )
                for out, g in zip(output_ids, batch['labels']):
                    pred.append(set([i for i in out]))
                    gold.append([])
                    g = g.view(-1, num_class)
                    for ll in g:
                        for i, l in enumerate(ll):
                            if l == 1:
                                gold[-1].append(i)
        scores = evaluate(pred, gold, id_to_label)
        macro_f1 = scores['macro_f1']
        micro_f1 = scores['micro_f1']
        print('macro', macro_f1, 'micro', micro_f1)
        if args.wandb:
            wandb.log({'val_macro': macro_f1, 'val_micro': micro_f1})
        early_stop_count += 1
        if macro_f1 > best_score_macro:
            best_score_macro = macro_f1
            save(macro_f1, best_score_macro, os.path.join('checkpoints', args.name, 'checkpoint_best_macro.pt'))
            early_stop_count = 0

        if micro_f1 > best_score_micro:
            best_score_micro = micro_f1
            save(micro_f1, best_score_micro, os.path.join('checkpoints', args.name, 'checkpoint_best_micro.pt'))
            early_stop_count = 0
        # save(macro_f1, best_score, os.path.join('checkpoints', args.name, 'checkpoint_{:d}.pt'.format(epoch)))
        save(micro_f1, best_score_micro, os.path.join('checkpoints', args.name, 'checkpoint_last.pt'))
        if args.wandb:
            wandb.log({'best_macro': best_score_macro, 'best_micro': best_score_micro})

        # torch.cuda.empty_cache()

    # test
    test = DataLoader(dataset['test'], batch_size=8, shuffle=False)
    model.eval()


    def test_function(extra):
        checkpoint = torch.load(os.path.join('checkpoints', args.name, 'checkpoint_best{}.pt'.format(extra)),
                                map_location='cpu')
        model.load_state_dict(checkpoint['param'])
        pred = []
        gold = []
        with torch.no_grad(), tqdm(test) as pbar:
            for batch in pbar:
                batch = {k: v.to('cpu') for k, v in batch.items()}
                output_ids, logits = model.generate(batch['input_ids'], depth2label=depth_to_id, )
                for out, g in zip(output_ids, batch['labels']):
                    pred.append(set([i for i in out]))
                    gold.append([])
                    g = g.view(-1, num_class)
                    for ll in g:
                        for i, l in enumerate(ll):
                            if l == 1:
                                gold[-1].append(i)
        scores = evaluate(pred, gold, id_to_label)
        macro_f1 = scores['macro_f1']
        micro_f1 = scores['micro_f1']
        print('macro', macro_f1, 'micro', micro_f1)
        with open(os.path.join('checkpoints', args.name, 'result{}.txt'.format(extra)), 'w') as f:
            print('macro', macro_f1, 'micro', micro_f1, file=f)
            prefix = 'test' + extra
        if args.wandb:
            wandb.log({prefix + '_macro': macro_f1, prefix + '_micro': micro_f1})


    test_function('_macro')
    # test_function('_micro')
