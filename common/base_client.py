"""基础层：Requests 统一请求封装
- Session 会话保持（自动管理 Cookie）
- 统一超时 / 重试 / 异常捕获
- 请求与响应全量日志
"""
import time
import requests

from common.config_loader import get_config
from common.logger import get_logger

logger = get_logger()


class BaseClient:
    def __init__(self):
        self.conf = get_config()
        self.base_url = self.conf["base_url"].rstrip("/")
        self.session = requests.Session()
        self.timeout = 15
        self.max_retry = 3

    def request(self, method, path, **kwargs):
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)
        last_err = None

        for attempt in range(1, self.max_retry + 1):
            try:
                logger.info(">>> [%s] %s kwargs=%s (attempt %s)", method.upper(), url, kwargs, attempt)
                start = time.time()
                resp = self.session.request(method, url, **kwargs)
                cost = round((time.time() - start) * 1000, 2)
                logger.info("<<< [%s] status=%s cost=%sms body=%s",
                            method.upper(), resp.status_code, cost, resp.text[:500])
                return resp
            except requests.RequestException as e:
                last_err = e
                logger.warning("请求异常(第%s次): %s", attempt, e)
                time.sleep(1)
        raise ConnectionError(f"重试 {self.max_retry} 次仍失败: {url}, err={last_err}")

    def get(self, path, **kw):
        return self.request("GET", path, **kw)

    def post(self, path, **kw):
        return self.request("POST", path, **kw)

    def put(self, path, **kw):
        return self.request("PUT", path, **kw)

    def delete(self, path, **kw):
        return self.request("DELETE", path, **kw)

    def close(self):
        self.session.close()
