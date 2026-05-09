## MinHash
## MinHashLSH
## SimHash
# 数据清洗pipeline
```python
1. 导入模块
import re  # 正则表达式，用于文本匹配和清理。
import hashlib  # 用于生成 MD5 哈希值，执行精确去重。
import jieba  # 中文分词工具，将句子切分为词汇。
import pandas as pd  # 数据处理库，用于读取 CSV 和处理表格数据。
from simhash import Simhash  # SimHash 算法库，用于短文本模糊去重。
from datasketch import MinHash, MinHashLSH  # MinHash LSH 库，用于海量长文本模糊去重。
2. 启发式过滤 (Heuristic Filtering)
这部分通过简单的统计规则剔除“不像人话”的垃圾数据。
def heuristic_filter(text: str) -> bool:
    if not text or len(text.strip()) == 0:  # 剔除空字符串或全是空格的文本。
        return False
    if len(text) < 5 or len(text) > 20000:  # 长度过滤：太短没信息量，太长可能是机器堆砌。
        return False
    # 匹配非字母、数字、中文和空格的特殊符号。
    pat = re.compile(r'[^a-zA-Z0-9\u4e00-\u9fa5\s]')
    special = len(pat.findall(text))
    ratio = special / len(text) if len(text) else 1
    if ratio > 0.3:  # 如果特殊符号占比超过 30%，判定为乱码或加密文本，剔除。
        return False
    if re.search(r'(.)\1{5,}', text):  # 检查是否有连续重复 5 次以上的字符（如“啊啊啊啊啊啊”），剔除。
        return False
    return True
3. 文本归一化 (Normalization)
def text_normalize(text: str) -> str:
    # 将多个连续的空格、换行、制表符压缩为一个空格，并去除首尾空格。
    text = re.sub(r'\s+', ' ', text).strip()
    return text
4. 质量过滤 (Quality Filtering)
def quality_filter(text: str) -> bool:
    # 统计非单词字符（空格、标点等）的占比。
    non_word = len(re.findall(r'[\s\W]', text)) / len(text) if len(text) else 1
    if non_word > 0.65:  # 如果标点和空格太多（超过 65%），说明文本质量极低，剔除。
        return False
    return True
5. 精确去重 (Exact Deduplication)
def exact_dedup(texts):
    seen = set()  # 存储已见过的 MD5 指纹。
    res = []
    for t in texts:
        # 计算文本的 MD5 值（比直接存长文本省内存）。
        md5 = hashlib.md5(t.encode("utf-8")).hexdigest()
        if md5 not in seen:
            seen.add(md5)
            res.append(t)
    return res
6. 中文分词
def tokenize_chinese(text):
    return list(jieba.cut(text))  # 使用 jieba 将中文文本切成词列表，这是计算模糊指纹的前提。
7. SimHash 去重 (适合短文本)
def simhash_dedup(texts, distance=3):
    keep = []
    sim_list = []
    for text in texts:
        tokens = tokenize_chinese(text)
        sh = Simhash(" ".join(tokens))  # 计算文本的 SimHash 指纹。
        flag = True
        for s in sim_list:
            # 计算汉明距离，如果距离 <= 3，认为两文高度相似。
            if sh.distance(s) <= distance:
                flag = False
                break
        if flag:
            keep.append(text)
            sim_list.append(sh)
    return keep
8. MinHash LSH 去重 (适合长文本/工业级)
def minhash_dedup(texts, threshold=0.75):
    # Jaccard相似度阈值，默认0.75，判定为相似/重复，取值范围：0-1，值越大，去重越严格
    # 将词列表转化为 2-shingles（相邻两个词组成的集合）。
    def get_shingles(tokens, n=2):
        return ["_".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
    
    # 初始化 LSH 索引，设置 Jaccard 相似度阈值为 0.75。
    # num_perm=128：随机置换次数，与MinHash的置换数保持一致，常见取值：64/128/256
    lsh = MinHashLSH(threshold=threshold, num_perm=128)
    mh_dict = {} # 存储每个文本的MinHash对象，键为文本索引idx,值为对应的MinHash实例
    for idx, text in enumerate(texts):
        tokens = tokenize_chinese(text) #jieba切分分词
        shingles = get_shingles(tokens) #调用get_shingle生成当前文本的2-shingle列表
        m = MinHash(num_perm=128)  # 创建 128 个随机置换的 MinHash。
        for s in shingles:
            m.update(s.encode("utf-8")) #将当前shingle加入MinHash计算，更新指纹
        lsh.insert(idx, m)  # 将指纹插入 LSH 桶中。
        mh_dict[idx] = m  #将当前文本的MinHash对象存入字典，方便后续查询
        
    visited = set()  # 空集合，用于记录已被标记为相似/重复的文本索引，避免重复处理
    keep = []   # 空列表，用于存储最终保留的不重复文本
    for idx in range(len(texts)):
        if idx in visited: continue  # 如果当前索引已被标记为访问过，则跳过避免重复保留
        # 查询 LSH 桶，找出所有与当前文本相似的文本 ID。
        for nid in lsh.query(mh_dict[idx]): # 查询LSH索引，返回所有与当前指纹相似的文本索引列表
            visited.add(nid)  # 将相似的文本全部标记为已访问。
        keep.append(texts[idx])  # 只保留每组相似文本中的第一篇。
    return keep
9. 流水线编排 (Pipeline)
def clean_pipeline(raw_texts, use_simhash=True):
    # 步骤 1 & 2：归一化并执行启发式过滤。
    step1 = [text_normalize(t) for t in raw_texts if heuristic_filter(t)]
    # 步骤 3：质量过滤。
    step2 = [t for t in step1 if quality_filter(t)]
    # 步骤 4：精确去重。
    step3 = exact_dedup(step2)
    # 步骤 5：根据选择执行 SimHash 或 MinHash 模糊去重。
    return simhash_dedup(step3) if use_simhash else minhash_dedup(step3)
10. 数据读取模块
def read_txt(path):
    with open(path,"r",encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def read_csv(path, col="text"):
    # 读取 CSV，剔除指定列为空的行，并转为列表。
    df = pd.read_csv(path).dropna(subset=[col])
    return df[col].tolist()

def read_json(path, key="text"):
    import json
    res = []
    with open(path,"r",encoding="utf-8") as f:
        for line in f:
            d = json.loads(line.strip())  # 逐行读取 JSONL 格式。
            if d.get(key):
                res.append(d[key])
    return res
11. 程序入口
if __name__ == "__main__":
    raw = read_txt("input.txt")  # 读取原始数据。
    clean = clean_pipeline(raw, use_simhash=True)  # 执行清洗流水线。
    with open("clean_result.txt","w",encoding="utf-8") as f:
        for line in clean:
            f.write(line+"\n")  # 保存结果。
    print("原始：",len(raw)," 清洗后：",len(clean))  # 打印清洗前后的对比。
```
