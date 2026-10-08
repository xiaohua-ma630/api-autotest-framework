"""业务层：按模块封装接口，用例层不接触 URL / 参数细节"""
from common.base_client import BaseClient


class HttpBinApi(BaseClient):
    """httpbin.org 公共演示接口（可替换为任意业务系统）"""

    # ---- 认证模块 ----
    def get_bearer_token(self, token):
        """Token 鉴权示例"""
        return self.get("/bearer", headers={"Authorization": f"Bearer {token}"})

    # ---- 请求结构模块 ----
    def get_headers(self, extra_headers=None):
        return self.get("/headers", headers=extra_headers or {})

    def post_json(self, payload):
        return self.post("/post", json=payload)

    def get_status(self, code):
        """返回指定状态码，用于状态码断言场景"""
        return self.get(f"/status/{code}")

    def get_delay(self, seconds):
        """延迟响应，用于超时/重试验证"""
        return self.get(f"/delay/{seconds}")

    # ---- 动态数据模块 ----
    def get_uuid(self):
        return self.get("/uuid")

    def get_ip(self):
        return self.get("/ip")
