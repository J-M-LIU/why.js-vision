import pandas as pd
import networkx as nx
import numpy as np
import random
from tqdm import tqdm
from sklearn.decomposition import PCA
import pprint
from gensim.models import Word2Vec
import warnings

warnings.filterwarnings('ignore')

# read the dataset
df = pd.read_csv("E://study/weather/space_data.tsv", sep="\t")
print(df.head())

G = nx.from_pandas_edgelist(df, "source", "target", edge_attr=True, create_using=nx.Graph())

G = nx.from_pandas_edgelist(df, "source", "target", edge_attr=True, create_using=nx.Graph())

print('The number of nodes in pur graph: ', len(G))


def get_randomwalk(node, path_length):
    random_walk = [node]

    for i in range(path_length - 1):
        temp = list(G.neighbors(node))
        temp = list(set(temp) - set(random_walk))
        if len(temp) == 0:
            break

        random_node = random.choice(temp)
        random_walk.append(random_node)
        node = random_node

    return random_walk


print('\n\nRandom sequence of nodes generated from Random Walk\n\n')
while True:
    first_node = input("Enter name of first node (for example 'space exploration') : ")
    if len(first_node) > 0:
        break
pprint.pprint(get_randomwalk(first_node, 10))

# 从图中获取所有节点的列表
all_nodes = list(G.nodes())

random_walks = []
for n in tqdm(all_nodes):
    for i in range(5):
        random_walks.append(get_randomwalk(n, 10))

# 序列长度
len(random_walks)

# 训练skip-gram (word2vec)模型
model = Word2Vec(window=4, sg=1, hs=0,
                 negative=10,  # 负采样
                 alpha=0.03, min_alpha=0.0007,
                 seed=14)

model.build_vocab(random_walks, progress_per=2)

model.train(random_walks, total_examples=model.corpus_count, epochs=20, report_delay=1)
print('\n\n Get similar nodes\n\n')
while True:
    any_node = input("Enter name of any node (for example 'space toursim') : ")
    if len(any_node) > 0:
        break
pprint.pprint(model.wv.similar_by_word(any_node))

