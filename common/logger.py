"""日志封装：同时输出到控制台与 logs/ 目录"""
import logging
import os
import time


def get_logger(name="api-test"):
    logger = logging.getLogger(name)
    if logger.handlers:            # 避免重复添加 handler
        return logger
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S")

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    fh = logging.FileHandler(
        os.path.join(log_dir, f"run_{time.strftime('%Y%m%d_%H%M%S')}.log"), encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return logger
