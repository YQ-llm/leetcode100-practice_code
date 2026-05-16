import re
import fasttext

class HeuristicFilter:
    def __init__(self, model_path):
        # 加载 FastText 进行语种识别，这是大模型语料清洗的标配
        self.lang_model = fasttext.load_model(model_path)

    def is_clean(self, text: str) -> bool:
        """多维度质量过滤"""
        # 1. 长度校验
        if not (100 <= len(text) <= 30000): return False
        
        # 2. 乱码/符号比率校验
        symbol_ratio = len(re.findall(r'[^\u4e00-\u9fa5a-zA-Z0-9]', text)) / len(text)
        if symbol_ratio > 0.3: return False
        
        # 3. 语种校验：只保留高置信度的中文
        label, score = self.lang_model.predict(text.replace('\n', ' '), k=1)
        if label[0] != '__label__zh' or score[0] < 0.8: return False
        
        # 4. 广告黑名单
        if re.search(r'加微信|优惠券|代购', text): return False
        
        return True
