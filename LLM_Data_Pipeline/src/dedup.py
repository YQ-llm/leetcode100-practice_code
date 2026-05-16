 # 阶段四：模糊去重 (MinHash LSH)
import hashlib
from datasketch import MinHash, MinHashLSH

class DedupEngine:
    def __init__(self, threshold=0.8, num_perm=128):
        # 1. 精确去重的哈希表 (存储 MD5)
        self.seen_md5 = set()
        # 2. 模糊去重引擎
        self.lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
        self.num_perm = num_perm

    def is_exact_duplicate(self, text: str) -> bool:
        """MD5 精确去重"""
        md5 = hashlib.md5(text.encode("utf-8")).hexdigest()
        if md5 in self.seen_md5:
            return True
        self.seen_md5.add(md5)
        return False

    def get_minhash(self, text: str) -> MinHash:
        """生成 MinHash 指纹"""
        m = MinHash(num_perm=self.num_perm)
        # 建议：长文本建议用 5-gram 或 9-gram，短文本用 3-gram
        shingles = {text[i:i+3] for i in range(len(text)-2)}
        for s in shingles:
            m.update(s.encode('utf8'))
        return m

    def is_fuzzy_duplicate(self, doc_id: str, m: MinHash) -> bool:
        """MinHash LSH 模糊去重"""
        if self.lsh.query(m):
            return True
        self.lsh.insert(doc_id, m)
        return False
