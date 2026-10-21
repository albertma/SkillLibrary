# styled-editor

固定文风的公众号写手：把大纲、思考、灵感素材写成约 2000 字的微信公众号文章，自动生成油画风格封面插图，按固定模板导出 HTML，并给出爆款改进建议。

遵循 Agent Skills 规范，同一份文件可直接在 pi agent、workbuddy、hermes agent 之间复用。

## 结构

```text
styled-editor/
├── SKILL.md             # 主指令：九步工作流
├── README.md            # 本文件
├── references/
│   ├── style-samples.md # 风格样本库（文风锚点，换成你自己的文章）
│   ├── style-profile.md # 风格画像（首次运行自动生成/更新）
│   ├── writing-rules.md # 平实语言硬规则（无黑话/短句/不倒装/引用标出处）
│   ├── viral-techniques.md # 爆款写作技巧清单
│   └── image-prompt.md  # 油画封面插图提示词公式
├── assets/
│   └── article-template.html # 固定格式 HTML 输出模板（九个占位符 + 六种组块）
├── scripts/
│   ├── gen-image.sh     # 调文生图接口出油画插图（默认智谱 CogView）
│   └── inject-env.sh    # 把 .env 固定值注入已生成的 HTML
├── .env.example         # 固定值配置模板（复制为工作目录的 .env）
└── docs/
    └── integration.md   # 对接 workbuddy / pi / hermes 的说明
```

## 快速开始

```bash
# 1. 在你写文章的工作目录建配置
cp styled-editor/.env.example .env   # 改 ACCOUNT_NAME（公众号名）等三个值

# 2. 触发（pi agent）
/skill:styled-editor 这是我的大纲：……

# 3. 产出（固定顺序）
#    风格画像 → 1800-2200 字正文 → 油画封面插图 → output/日期-slug.html → 爆款建议 + 3 个备选标题
```

发布：浏览器打开 HTML → 全选复制 → 粘贴进公众号编辑器，样式和图片一起带过去。

## 在哪里改什么

| 想改什么 | 改哪里 |
|---|---|
| 公众号名、页脚签名、结尾转发语 | 工作目录 `.env`（生成时注入） |
| 插图生成接口 / 模型 / key | 工作目录 `.env` 的 IMAGE_* 三项（不配则复用 `~/.pi/agent/models.json` 的智谱 key） |
| 颜色、字号、版式 | `assets/article-template.html` 的 style 值 |
| 封面插图风格 | `references/image-prompt.md` 的风格描述 |
| 文风 | `references/style-samples.md` 换成自己的文章，然后删 `references/style-profile.md` |
| 写作硬规则 | `references/writing-rules.md` |

## 硬规则（每次自检）

- 平实语言，不用黑话；术语必须当场用大白话解释
- 一句不超过 40 字；不写倒装句
- 引用他人原话必须标出处，与自己的评论严格区分
- 全文 1800-2200 字

## 对接细节

见 `docs/integration.md`（pi / workbuddy / hermes 的安装位置和验证方法）。
