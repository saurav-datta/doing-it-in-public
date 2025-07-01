---
title: file_format_others
draft: false
tags:
  - file_format
  - pgm-index
  - rmi
  - alex
  - lisa
  - lider
---
| Index     | Example Use Case                | Real-world System / Research        | Supports Updates? | Best Use                          |
| --------- | ------------------------------- | ----------------------------------- | ----------------- | --------------------------------- |
| PGM-Index | Token maps, static document IDs | Umbra, DuckDB, Lucene optimizations | NO                | Fast sorted-key lookup            |
| ALEX      | Key-value stores with updates   | Microsoft FasterKV, TSDB            | YES               | High-throughput dynamic datasets  |
| RMI       | Sorted metadata, timestamps     | Google Search infra                 | NO                | Custom two-layer regression index |
| LISA      | Embedding/vector retrieval      | Milvus (inspired), Weaviate layers  | YES               | ANN on high‑dimensional data      |
| LIDER     | Token-doc matching in RAG       | ORQA, Microsoft retrieval systems   | ?                 |                                   |


| Index     | Python-ready?             |
| --------- | ------------------------- |
| PGM‑Index | ✅ (`pygm`)                |
| RMI       | ✅ (custom implementation) |
| ALEX      | ⚠️ (C++ only)             |
| LISA      | ⚠️ (C++/academic)         |
# LIDER
<small>https://arxiv.org/abs/2205.00970</small>
- most of the existing learned indexes are designed for low dimensional data, which are not suitable for dense passage retrieval with high-dimensional dense embeddings
- includes 
	- an adapted recursive model index (RMI) and 
	- a dimension reduction component which consists 
		- of an extended SortingKeys-LSH (SK-LSH) and 
		- a key re-scaling module
- dimension reduction component reduces the high-dimensional dense embeddings into one-dimensional keys and sorts them in a specific order,
	- which are then used by the RMI to make fast prediction
# PGM‑Index (via PyGM)
```python
import pygm
data = list(range(0, 1000000, 3))  # sorted integer keys
pgm = pygm.SortedList(data, epsilon=64)

# exact lookup
print(42 in pgm)         # True/False
# position estimation
pos = pgm.bisect_left(5000)
print(data[pos])
# range query
print(list(pgm.range(100, 200)))

```

# RMI (Recursive Model Index)
Trains a small regression model to predict positions in sorted array

Simplified example:
```python
import numpy as np
from sklearn.linear_model import LinearRegression

keys = np.sort(np.random.randint(0, 1000000, size=100000))
positions = np.arange(len(keys))

# Level 1: coarse predictor
l1 = LinearRegression().fit(keys.reshape(-1,1), positions)
l1_preds = l1.predict(keys.reshape(-1,1)).astype(int)
# train leaf-level models: one per bucket
leaf_models = {}
for bucket_id in range(10):
    mask = l1_preds // (len(keys)//10) == bucket_id
    sub_keys = keys[mask]
    sub_pos = positions[mask]
    if len(sub_keys):
        leaf = LinearRegression().fit(sub_keys.reshape(-1,1), sub_pos)
        leaf_models[bucket_id] = leaf

# lookup
def rmi_lookup(x):
    b = int(l1.predict([[x]])[0]) // (len(keys)//10)
    leaf = leaf_models.get(b)
    return int(leaf.predict([[x]])[0]) if leaf else None

```



# 