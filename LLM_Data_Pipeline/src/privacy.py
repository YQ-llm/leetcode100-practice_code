import re

class PrivacyGuard:
    def __init__(self):
        # 定义常见敏感信息的正则模式
        # 1. 手机号 (匹配 13/14/15/17/18/19 开头的 11 位数字)
        self.phone_pattern = re.compile(r'1[3-9]\d{9}')
        # 2. 邮箱地址
        self.email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        # 3. 身份证号 (简单的18位验证，实际场景可接入更专业的正则)
        self.id_card_pattern = re.compile(r'[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]')

    def anonymize(self, text: str) -> str:
        """对文本进行脱敏处理"""
        # 将匹配到的信息替换为特定的标记
        text = self.phone_pattern.sub("[PHONE]", text)
        text = self.email_pattern.sub("[EMAIL]", text)
        text = self.id_card_pattern.sub("[ID_CARD]", text)
        return text
