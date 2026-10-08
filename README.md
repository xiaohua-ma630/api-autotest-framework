# 接口自动化测试框架（Pytest + Requests + Allure + Jenkins）

## 快速开始
```bash
pip install -r requirements.txt
pytest                # 执行全部用例
allure serve report/allure-results   # 本地查看报告
```

## 框架分层
- common/base_client.py   基础层：Session/重试/日志
- api/                    业务层：按模块封装接口
- testcases/              用例层：参数化 + 三重断言
- data/                   YAML 数据驱动
- config/config.yaml      多环境配置

## Jenkins
Jenkinsfile 已内置：定时构建、Allure 报告发布、失败邮件通知。
