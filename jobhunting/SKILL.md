---
name: jobhunting
description: 操作个人求职 Agent：抓取远程职位、按用户画像评分排序、LLM 深度匹配分析与定制 Cover Letter、投递跟进提醒、每日推送飞书/Telegram。Use when the user mentions job hunting, wants to check today's job digest, analyze a job's fit, draft an application or cover letter, or manage application follow-ups.
---

# jobhunting：个人求职管家

你是一个求职助手的操作员，通过本目录下的 CLI 工具（`main.py`）帮用户管理找工作全流程：发现职位 → 匹配评分 → 深度分析 → 生成申请材料 → 投递跟进。

## 环境准备（首次使用必做）

1. 在本 skill 目录下建虚拟环境并安装依赖：
   ```bash
   uv venv .venv && uv pip install -r requirements.txt --python .venv/bin/python
   ```
   （或 `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`）
2. 检查 `profile.yaml`（用户画像）和 `config.yaml`（抓取源、评分、通知）是否存在。都不存在时先跑 `.venv/bin/python main.py init` 交互式生成；缺一个时对照 `profile.example.yaml` 补
3. LLM 功能（`chat --fit` / `chat --draft`）需要 `.env` 里的 `LLM_API_KEY` 等配置，模板见 `.env.example`；没有时这些命令会降级或不可用，但 `run` / `list` / `draft` / 跟踪命令照常工作

## 每日工作流

严格按用户意图选命令，所有命令都在本目录下用 `.venv/bin/python main.py <命令>` 执行：

| 用户说 | 命令 |
|---|---|
| "拉一下今天的职位" / "跑一轮" | `run --push`（抓取→评分→入库→推送） |
| "看看最近有哪些职位" | `list -n 20` |
| "这个职位跟我匹配吗" | `chat --fit <job_id>`（LLM 读 JD + 画像给真实匹配分） |
| "帮我写封求职信" | `chat --draft <job_id>`（LLM 定制 Cover Letter） |
| "这个职位的问题" | `chat <job_id> "问题"`（单次问答） |
| "快速评估一下"（无 LLM） | `draft <job_id>`（本地模板：匹配结论 + 简历建议 + 面试题） |
| "我投了 xxx" | `applied <job_id>`（启动跟进计时） |
| "对方回复了" | `replied <job_id>`（停止提醒） |
| "哪些投递没回音" | `followups` |

`job_id` 从 `list` 或每日推送的摘要里取，格式如 `remoteok:remote-xxx-123`。

## 交互模式

用户想连续操作多个职位时，启动 REPL：`.venv/bin/python main.py agent`（内部支持 /fit /draft /resume /apply）。你也可以代替用户逐条执行 CLI 命令，把输出整理成易读的摘要。

## 评分调优

用户抱怨"推的职位不对味"时：

1. 看 `config.yaml` 的 keywords（核心词进标题 ×20 是最强信号）、region、threshold（默认 40）
2. 改完后跑 `.venv/bin/python main.py rescore` 重算历史分数
3. 评分规则明细见 `README.md` 的 "How scoring works"

## 排障

- 抓取失败：单源失败正常（自动跳过），全部失败会告警；网络问题优先重跑一次 `run`
- `chat` 报 LLM 错误：检查 `.env` 的 `LLM_BASE_URL`/`LLM_API_KEY`，MiniMax 国内直连，DeepSeek 需代理
- 数据都在 `data/jobs.db`（SQLite，自动清理），日志在 `logs/`
- 定时推送：crontab 工作日 09:00，示例见 `README.md` 的 "Automate"

## 维护说明

- 完整功能文档：`README.md`；架构与数据流：`docs/architecture.html`
- 个人隐私文件不入库：`profile.yaml`、`.env`、`web3career_profile.yaml`、`drafts/`、`data/`、`logs/`、`resume/`（均已在 `.gitignore`）
- 新职位源：在 `src/jobhunting/sources/` 子类化 `JobSource`，实现 `fetch()` + `normalize()`；不要加 LinkedIn/Indeed 爬虫（违反 ToS）
- 历史版本：https://github.com/albertma/jobhunting-agent
- 所有路径用本 skill 目录内相对路径，不依赖任何 agent 私有功能
