---
title: jsonl
draft: false
tags:
  - jsonl
  - file_format
  - json
---

# Highlights
JSONL stands for JSON Lines
Also called newline-delimited JSON
Each line is a valid JSON 

# Example 1
```json
{"name": "Gilbert", "session": "2013", "score": 24, "completed": true}
{"name": "Alexa", "session": "2013", "score": 29, "completed": true}
{"name": "May", "session": "2012B", "score": 14, "completed": false}
{"name": "Deloise", "session": "2012A", "score": 19, "completed": true}
```

# Example 2
```json
{"name": "Gilbert", "wins": [["straight", "7♣"], ["one pair", "10♥"]]}
{"name": "Alexa", "wins": [["two pair", "4♠"], ["two pair", "9♠"]]}
{"name": "May", "wins": []}
{"name": "Deloise", "wins": [["three of a kind", "5♣"]]}
```

# Example 3
[[zcode/jsonl_demo.py]]

# Example 4 - OpenAI format
As shown in https://dev.to/es404020/understanding-the-openai-jsonl-format-organising-the-records-24mc

```python
 openai_format = {
        "message":[
            {"role":"system","content":system},
            {"role":"user","content":""},
            {"role":"assistant","content":""}
        ]
    }
```

```python
import  json
df = pd.read_csv('/content/dataset/train.csv', on_bad_lines='skip')

final_df = df.head(150)
total_tokens = cal_num_tokens_from_df(final_df,'gpt-3.5-turbo')
print(f"total {total_tokens}")


system ="You are a intelligent assistant designed to classify news articles into three categories :business ,entertainment,sport,tech,politics"
with open('dataset/train.jsonl','w') as f:
  for _,row in final_df.iterrows():
    openai_format = {
        "message":[
            {"role":"system","content":system},
            {"role":"user","content":row['text']},
            {"role":"assistant","content":row['label']}
        ]
    }
    json.dump(openai_format,f)
    f.write('\n')
```

Response
```python
{"message": [{"role": "system", "content": "You are a intelligent assistant designed to classify news articles into three categories :business ,entertainment,sport,tech,politics"}, {"role": "user", "content": "qantas considers offshore option australian airline qantas could transfer as"}, {"role": "assistant", "content": "business"}]}
```
**Reference**
 - https://jsonlines.org/
 - https://dev.to/es404020/understanding-the-openai-jsonl-format-organising-the-records-24mc
 
