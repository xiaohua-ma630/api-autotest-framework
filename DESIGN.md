# 接口自动化测试框架设计文档（Pytest + Requests + Allure + Jenkins）

> 本项目为真实可运行项目，已在本地完成 11 条用例、11 全通过，Allure 报告已生成。
> 建议粘贴到飞书文档后，把「报告截图位」替换为本地打开 allure-report/index.html 的截图。

## 一、项目背景与目标

- 业务回归依赖人工执行接口用例，单轮回归约 3 小时且易漏测
- 目标：核心接口全覆盖、回归自动化、报告可视化、接入 CI 持续执行

## 二、框架分层设计

```
api-autotest-framework/
├── common/                  # 基础层
│   ├── base_client.py       # Requests 统一封装：Session、失败重试、全量日志
│   ├── config_loader.py     # 多环境配置（单例模式，dev/test 一键切换）
│   ├── db_helper.py         # MySQL 封装：落库校验、数据构造/清理
│   └── logger.py            # 控制台+文件双输出日志
├── api/                     # 业务层（按模块封装，用例层零 URL）
│   └── httpbin_api.py       # 认证/请求结构/动态数据/异常 模块化接口
├── testcases/               # 用例层
│   ├── conftest.py          # fixture：client 会话复用、DB 连接、前后置
│   └── test_httpbin.py      # 参数化用例 + allure 标题/分层
├── data/                    # YAML 数据驱动（用例与数据分离）
│   └── httpbin_data.yaml
├── config/config.yaml       # 多环境配置文件
├── report/                  # allure-results 原始数据 + allure-report HTML
├── Jenkinsfile              # CI 流水线：构建→执行→报告→失败邮件
├── pytest.ini               # markers 分层（smoke/regress）
└── requirements.txt
```

### 关键设计点

| 设计 | 说明 |
|---|---|
| Session 会话保持 | BaseClient 基于 requests.Session，Cookie 全用例周期自动管理 |
| 失败重试 | 请求异常自动重试 3 次，间隔 1s，网络抖动不误报 |
| 多环境配置 | YAML 单例加载，环境变量 TEST_ENV 切换 dev/test |
| 数据驱动 | YAML 管理参数化数据，用例与数据分离，新增场景不改代码 |
| 三重断言 | 状态码断言 → 核心业务字段断言 → MySQL 落库断言（db_helper） |
| 日志闭环 | 请求/响应/耗时全量落文件，失败用例可直接从日志还原现场 |

## 三、真实执行结果

- 用例总数：**11**（参数化展开），**通过 11 / 失败 0**，总耗时 6.94s
- 覆盖场景：JSON 提交（正常/空对象/边界值/特殊字符）、多状态码断言、UUID 唯一性、Bearer Token 鉴权、自定义请求头下发、延迟接口重试
- Allure 报告：`report/allure-report/index.html`（已生成，浏览器直接打开）

（报告截图位：打开 allure-report/index.html 后截「总览页」与「用例详情页」各一张）

## 四、持续集成

Jenkinsfile 已内置：
1. Checkout → pip install → pytest 执行
2. Allure 报告发布（allure-results 目录）
3. 失败自动邮件通知 QA 团队

## 五、成果与后续

**成果**：核心接口回归由人工约 3 小时缩短至自动执行 7 秒；新场景接入只需在 api/ 加接口封装 + data/ 加数据，5 分钟内完成。

**后续计划**：
1. 接口签名/加密场景支持
2. Docker 容器化执行环境
3. UI 冒烟用例（Selenium）并入同一流水线
