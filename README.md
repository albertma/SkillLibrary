# SkillLibrary

Agent Skills 库。每个子目录是一个独立 skill，遵循 [Agent Skills 规范](https://agentskills.io)，可在 pi agent、workbuddy、hermes agent 等支持该规范的 agent 之间直接复用。

## Skills

| Skill | 说明 |
|---|---|
| [styled-editor](styled-editor/) | 固定文风的公众号写手：把大纲、思考、灵感写成约 2000 字的微信公众号文章，油画封面插图 + 固定格式 HTML 导出 + 爆款建议 |
| [jobhunting](jobhunting/) | 求职管家：抓取远程职位、按画像评分、每日推送飞书/Telegram，LLM 深度匹配分析与定制 Cover Letter，投递跟进提醒 |
| [interview-prep](interview-prep/) | 算法面试教练：讲题（分步注释 + 复杂度 + 可视化）、出题、模拟面试，题解库随使用积累 |

## 安装

```bash
git clone https://github.com/albertma/SkillLibrary.git
cd SkillLibrary
./install.sh              # 列出可安装的 skills
./install.sh styled-editor  # 安装到 ~/.agents/skills/ 和 ~/.pi/agent/skills/
./install.sh --link styled-editor  # 软链安装（仓库改动即时生效）
```

## 新增一个 skill

1. 新建子目录，内含 `SKILL.md`（标准 frontmatter：name、description）
2. 引用文件一律用目录内相对路径，不依赖任何 agent 私有功能
3. 在上面的表格里加一行

## 约定

- skill 内的个人配置走 `.env`（参考各 skill 的 `.env.example`），`.env` 不入库
- 生成的产物（文章、图片）不入库
