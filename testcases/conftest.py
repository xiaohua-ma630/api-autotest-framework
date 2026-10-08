"""全局 fixture：登录态、客户端实例、DB 连接、allure 环境信息"""
import pytest

from api.httpbin_api import HttpBinApi
from common.base_client import BaseClient
from common.config_loader import get_config


@pytest.fixture(scope="session")
def conf():
    return get_config()


@pytest.fixture(scope="session")
def client():
    """session 级客户端：整个测试周期复用一个连接池"""
    c = HttpBinApi()
    yield c
    c.close()


@pytest.fixture(scope="session")
def db():
    """数据库连接（按需启用，配置好 db 后生效）"""
    try:
        from common.db_helper import DBHelper
        helper = DBHelper()
        yield helper
        helper.close()
    except Exception:
        yield None


@pytest.fixture(autouse=True)
def _allure_env(request):
    """每个用例自动附加 allure 标题"""
    marker = request.node.get_closest_marker("allure_label")
    yield
