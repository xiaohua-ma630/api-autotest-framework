"""数据库助手：MySQL 查询 / 落库校验 / 数据清理"""
import pymysql

from common.config_loader import get_config
from common.logger import get_logger

logger = get_logger()


class DBHelper:
    def __init__(self):
        conf = get_config()["db"]
        self.conn = pymysql.connect(
            host=conf["host"], port=int(conf["port"]),
            user=conf["user"], password=conf["password"],
            database=conf["database"], charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor, autocommit=True,
        )

    def query_one(self, sql, params=None):
        """查询单条，用于落库校验"""
        with self.conn.cursor() as cur:
            cur.execute(sql, params or ())
            row = cur.fetchone()
            logger.info("DB query_one: %s -> %s", sql, row)
            return row

    def query_all(self, sql, params=None):
        with self.conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()

    def execute(self, sql, params=None):
        """写操作：测试数据构造 / 清理"""
        with self.conn.cursor() as cur:
            rows = cur.execute(sql, params or ())
            logger.info("DB execute: %s affected=%s", sql, rows)
            return rows

    def close(self):
        self.conn.close()
