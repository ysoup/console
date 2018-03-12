# encoding=utf-8

import logging
import sys
# 程序级别日志
logger = logging.getLogger("test")
formatter = logging.Formatter('%(asctime)s %(levelname)-3s: %(message)s')
file_handler = logging.FileHandler("test.log")
file_handler.setFormatter(formatter)

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值
# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)




if __name__ == "__main__":
    logger.info("测试>>>>>>>>")


