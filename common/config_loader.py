"""多环境配置加载器"""
import os
import yaml


class ConfigLoader:
    _instance = None
    _config = None

    def __new__(cls):
        """单例：整个框架共享一份配置"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self, env=None):
        if self._config is not None and env is None:
            return self._config
        env = env or os.environ.get("TEST_ENV", "test")
        cfg_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
        with open(cfg_path, encoding="utf-8") as f:
            all_conf = yaml.safe_load(f)
        self._config = all_conf[env]
        self._config["env"] = env
        return self._config


def get_config():
    return ConfigLoader().load()
