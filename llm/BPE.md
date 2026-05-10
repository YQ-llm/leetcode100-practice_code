## 手动模拟BPE合并过程
```python
from collections import Counter

def simulate_bpe(words_with_freq, num_merges=5):
    """手动模拟 BPE 合并过程

    Args:
        words_with_freq: dict, 如 {"low": 5, "lower": 2, "newest": 6}
        num_merges: 合并次数，决定最终词表的大小，合并次数越多，词表里的长词/字词就越多
    """
    2. 初始化阶段
    vocab = set() #初始化词表，使用集合确保唯一性
    corpus = []    # 初始化语料库，用于存储拆分后的 token 序列
    for word, freq in words_with_freq.items():
        chars = list(word)   # 将单词拆解为单个字符，如 "low" -> ['l', 'o', 'w']
        vocab.update(chars)   # 将这些基础字符加入词表
        for _ in range(freq):
            corpus.append(chars.copy())  # 根据频率，将拆分后的单词重复存入语料库
      #以上作用：BPE 算法是从字符级别开始的。这一步把所有单词打碎成字母，并根据它们出现的次数准备好“实验材料”。
    print(f"初始词表({len(vocab)}): {sorted(vocab)}\n")
    3. 核心迭代循环（寻找并合并）
    for step in range(num_merges):  #A. 统计相邻对频率
        pair_freq = Counter()      # 创建计数器，统计相邻两个 token 出现的次数
        for tokens in corpus:
            for i in range(len(tokens) - 1):
                # 统计如 ('l', 'o') 这种组合出现的总次数
                pair_freq[(tokens[i], tokens[i + 1])] += 1
     
        if not pair_freq:
            break
        #以上作用：扫描整个语料库，看看哪两个 token 挨在一起的次数最多。
        best_pair, freq = pair_freq.most_common(1)[0]  #B. 找出“冠军”并更新词表# 找出频率最高的那一对
        new_sym = best_pair[0] + best_pair[1]   # 将它们合并成一个新 token
        vocab.add(new_sym)     # 将新 token 加入词表
        #参数含义：best_pair 是胜出的组合（如 ('e', 's')），new_sym 是合并后的新字符串（如 'es'）
        #C. 更新语料库（物理合并）
#这是代码中最复杂的部分，它遍历语料库，把所有的 best_pair 替换为 new_sym：
        new_corpus = []
        for tokens in corpus:
            merged = []
            i = 0
            while i < len(tokens):
                # 如果当前位置和下一个位置正好匹配“冠军组合”
                if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == best_pair:
                    merged.append(new_sym)  # 存入合并后的新 token
                    i += 2                 # 跳过两个位置
                else:
                    merged.append(tokens[i])   # 否则保留原样
                    i += 1
            new_corpus.append(merged)
        corpus = new_corpus                 # 用合并后的新语料库替换旧的
      #逻辑意义：这模拟了分词器进化的过程。原本模型只认识 e 和 s，现在它学会了一个新词 es。

        print(f"Step {step+1}: 合并 {best_pair} → '{new_sym}' (频率={freq})")
        print(f"  词表大小: {len(vocab)}")
        example = corpus[0]
        print(f"  示例: {example}\n")

simulate_bpe({"low": 5, "lower": 2, "newest": 6, "widest": 3}, num_merges=5)
        
```
