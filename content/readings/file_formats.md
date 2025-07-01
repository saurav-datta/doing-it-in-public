---
title: file_formats
draft: false
tags:
  - file_format
  - pgm-index
  - rmi
  - alex
  - lisa
  - lider
description: Useful file formats
---
- [Overview](#overview)
- [LIDER](#lider)
- [PGM‑Index (via PyGM)](#pgm%E2%80%91index-via-pygm)
- [RMI (Recursive Model Index)](#rmi-recursive-model-index)
- [Parquet + Arrow + External Index](#parquet--arrow--external-index)
- [WebDataset (TAR + Index)](#webdataset-tar--index)
- [Indexed JSONL / FASTER JSONL](#indexed-jsonl--faster-jsonl)
- [LMDB / RocksDB / LevelDB](#lmdb--rocksdb--leveldb)
- [Delta Lake / Apache Iceberg / Apache Hudi](#delta-lake--apache-iceberg--apache-hudi)
- [Petastorm (for Spark → PyTorch)](#petastorm-for-spark-%E2%86%92-pytorch)
- [Recommendation by Use Case](#recommendation-by-use-case)
- [References](#references)

# Overview

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
<small> https://pgm.di.unipi.it/ </small>

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


# Parquet + Arrow + External Index

- **Description**: Compressed columnar format with schema and fast filtering.
    
- **Indexing**: Partitioned (e.g. by time/shard/user), filter pushdown, row group metadata.
    
- **Used by**: Meta (via Presto, Velox), Hugging Face Datasets.
    
- **Pros**: Efficient I/O, column projection, multi-threaded.
    
- **Cons**: Slower random row-level access unless partitioned/indexed.
    

---

# WebDataset (TAR + Index)

- **Description**: .tar archive of samples; each sample can have `.txt`, `.json`, `.cls`, etc.
    
- **Indexing**: Pre-generated index files (e.g. `.idx` with byte offsets or keys).
    
- **Used by**: LAION, OpenCLIP, EleutherAI.
    
- **Pros**: Streamable, HTTP/S3 friendly, works with PyTorch.
    
- **Cons**: Needs preprocessing to build archives and indexes.
    

---

# Indexed JSONL / FASTER JSONL

- **Description**: JSONL with separate offset index (e.g., `.npy`, `.json`, RocksDB).
    
- **Used by**: MosaicML, internal Meta/Anthropic preprocessing tools.
    
- **Pros**: Random access with simple tooling.
    
- **Cons**: Manual index generation, JSON overhead.
    

---

# LMDB / RocksDB / LevelDB

- **Description**: Key–value stores backed by memory-mapped files.
    
- **Indexing**: Built-in B-tree or LSM tree.
    
- **Used by**: OpenAI (Whisper training), Meta (feature storage), DeepMind.
    
- **Pros**: Fast random access, ideal for retrieval-heavy workloads.
    
- **Cons**: Less friendly for distributed training unless chunked carefully.
    

---

# Delta Lake / Apache Iceberg / Apache Hudi

- **Description**: Data lake formats with transaction logs, versioning, and indexing.
    
- **Indexing**: Partitioning + manifest files + column stats.
    
- **Used by**: Databricks, Meta’s Hydra pipeline, enterprise ML workflows.
    
- **Pros**: Scalable, supports schema evolution, versioned data.
    
- **Cons**: Heavyweight for non-enterprise use; Spark or Trino often needed.
    

---

# Petastorm (for Spark → PyTorch)

- **Description**: Parquet with additional metadata for PyTorch training.
    
- **Indexing**: Shard + row group + partition-based.
    
- **Used by**: Uber, Meta, Netflix.
    
- **Pros**: Integrates with Spark + PyTorch DataLoader.
    
- **Cons**: Tied to PyArrow and Spark stack.
    

---

# Recommendation by Use Case

|Use Case|Recommended Format|
|---|---|
|Pretraining (scale: 100B+ tokens)|Parquet + Arrow + partitioned index|
|Fine-tuning (instruction pairs)|Indexed JSONL / WebDataset|
|Retrieval-heavy (QA, RLHF)|LMDB / RocksDB|
|Multimodal (text+image/audio)|WebDataset or Arrow bundles|
|Cloud data lake (versioned)||
# References
-  PGM <small>https://pgm.di.unipi.it/</small>
- LIDER <small>https://arxiv.org/abs/2205.00970</small>



 