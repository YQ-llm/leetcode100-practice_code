import re
import unicodedata

class TextNormalizer:
    def __init__(self):
        # 定义需要统一转换的标点符号映射 (半角转全角)
        self.punct_map = {
            "!": "！", "?": "？", ",": "，", 
            ".": "。", ";": "；", ":": "："
        }

    def normalize(self, text: str) -> str:
        """
        全流程文本归一化：
        1. Unicode 规范化 (NFKC)
        2. 空白字符压缩
        3. 标点符号统一
        4. 字符过滤
        """
        # 1. Unicode 标准化 (将变体字符转为标准形式)
        text = unicodedata.normalize('NFKC', text)
        
        # 2. 编码纠正 (处理部分错误的 UTF-8 字符)
        text = text.encode("utf-8", errors="ignore").decode("utf-8")
        
        # 3. 空白字符压缩 (将多个空格、tab、换行压缩为一个空格)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 4. 标点统一
        for eng, chn in self.punct_map.items():
            text = text.replace(eng, chn)
            
        # 5. 过滤掉控制字符 (ASCII 0-31 等不可见字符)
        text = re.sub(r'[\x00-\x1f\x7f]', '', text)
        
        return text
