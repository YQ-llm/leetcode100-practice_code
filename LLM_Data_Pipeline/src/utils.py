# 工具库：字节索引器、日志封装
import json, logging

def get_logger(name="Pipeline"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

class ByteOffsetIndexer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.offsets = [0]
        with open(file_path, 'rb') as f:
            while f.readline(): self.offsets.append(f.tell())
        self.offsets.pop()

    def get_line(self, index):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            f.seek(self.offsets[index])
            return json.loads(f.readline())

    def __len__(self): return len(self.offsets)

