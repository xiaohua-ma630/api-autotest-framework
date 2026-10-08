"""用例层：只写业务断言，不接触 URL 与请求细节
- 参数化覆盖正向 / 异常 / 边界
- allure 附加标题与步骤
"""
import allure
import pytest
import yaml

from pathlib import Path

DATA = yaml.safe_load(
    (Path(__file__).parent.parent / "data" / "httpbin_data.yaml").read_text(encoding="utf-8"))


@allure.epic("httpbin 演示服务")
@allure.feature("请求结构")
class TestPostJson:

    @allure.title("POST /post JSON提交：{desc}")
    @pytest.mark.parametrize("payload,expect_code,desc",
        [(c["payload"], c["expect_code"], c["desc"]) for c in DATA["post_json"]],
        ids=[c["desc"] for c in DATA["post_json"]])
    def test_post_json(self, client, payload, expect_code, desc):
        resp = client.post_json(payload)
        # 断言1：状态码
        assert resp.status_code == expect_code
        body = resp.json()
        # 断言2：核心业务字段（httpbin 会回显提交的 json）
        assert body["json"] == payload


@allure.epic("httpbin 演示服务")
@allure.feature("状态码")
class TestStatus:

    @allure.title("状态码场景：/{code}")
    @pytest.mark.parametrize("code", DATA["status_code"], ids=[str(c["code"]) for c in DATA["status_code"]])
    def test_status(self, client, code):
        resp = client.get_status(code["code"])
        assert resp.status_code == code["code"]


@allure.epic("httpbin 演示服务")
@allure.feature("动态数据")
class TestDynamic:

    @allure.title("GET /uuid 返回唯一 uuid")
    def test_uuid_unique(self, client):
        r1 = client.get_uuid().json()["uuid"]
        r2 = client.get_uuid().json()["uuid"]
        assert r1 != r2 and len(r1) == 36

    @allure.title("Token 鉴权校验")
    def test_bearer(self, client):
        token = "feibao-test-token"
        resp = client.get_bearer_token(token)
        assert resp.status_code == 200
        assert resp.json()["authenticated"] is True

    @allure.title("自定义请求头下发校验")
    def test_custom_header(self, client):
        resp = client.get_headers({"X-Feibao-Env": "pytest"})
        assert resp.status_code == 200
        assert resp.json()["headers"].get("X-Feibao-Env") == "pytest"


@allure.epic("httpbin 演示服务")
@allure.feature("异常与重试")
class TestAbnormal:

    @allure.title("延迟接口触发重试机制不崩溃")
    def test_delay_retry(self, client):
        resp = client.get_delay(1)
        assert resp.status_code == 200
