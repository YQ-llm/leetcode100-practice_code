# 阶段二：语种识别 (LID)
import fasttext
import os

class LanguageFilter:
    def __init__(self, model_path: str):
        self.model = fasttext.load_model(model_path) if os.path.exists(model_path) else None
    
    def is_chinese(self, text: str) -> bool:
        if not self.model: return True
        label, score = self.model.predict(text.replace('\n', ' '), k=1)
        return label[0] == '__label__zh' and score[0] > 0.8
