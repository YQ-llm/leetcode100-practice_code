# 工具库：字节索引器、日志封装

import logging

def get_logger(name="DataCleaner"):
    """配置全局日志系统，便于生产环境排查错误"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
