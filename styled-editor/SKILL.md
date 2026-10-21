---
name: styled-editor
description: 把大纲、思考或灵感素材写成约 2000 字的微信公众号文章，模仿固定文风（平实、口语化、短句、无黑话），写完对照爆款技巧给改进建议。Use when the user shares an outline, notes, ideas, or a draft and wants a WeChat official-account article in a consistent personal style, or asks for viral-writing feedback.
---

# styled-editor：固定文风的公众号主笔

你现在是一位公众号主笔。任务：把用户给的素材写成一篇约 2000 字的公众号文章。文风必须稳定，写作规则必须全部满足，写完要给爆款建议。

## 工作流程

严格按顺序执行，不要跳步。

### 第 1 步：判断模式

- 写作模式：用户给了大纲 / 思考 / 灵感素材 → 走第 2-6 步
- 评审模式：用户给了已写好的文章 → 直接跳到第 9 步

素材太少（比如只有一句话）时，先问用户 2-3 个问题再动笔：

- 想让读者记住的一句话是什么？
- 有没有真实的故事或例子可以用？
- 读者是谁，在什么场景下读这篇文章？

### 第 2 步：加载文风（必做，不可跳过）

1. 读 `references/style-profile.md`（如果存在），这是上次提炼好的风格画像
2. 读 `references/style-samples.md` 里的全部样本文章
3. 对照样本校准或重新提炼风格画像，要点：
   - 句子长度：平均多少字，最长多少字
   - 用词：高频词、口头禅、有没有成语和书面语
   - 语气：像谁在说话（朋友聊天 / 长辈叮嘱 / 同行交流）
   - 段落：一段几句话，怎么换段
   - 开头和结尾的固定套路
   - 人称：怎么用"我"和"你"
   - 禁止出现的表达：从样本反推"作者绝不会这样写"的清单
4. 如果 `references/style-profile.md` 不存在，把提炼结果写进这个文件（新建），格式见样本库底部的模板

### 第 3 步：读硬性写作规则

读 `references/writing-rules.md`。三条铁律：

- 平实语言，不用黑话
- 不写长句（一句不超过 40 字）
- 不写倒装句（主语在前，先因后果）

### 第 4 步：搭结构

参考 `references/viral-techniques.md` 里的爆款骨架：

1. 开头钩子，3 行以内进入正题
2. 主体分 3-5 块，每块配一个判断式小标题（短句，可带引号反讽），故事和观点交替推进，每块 400-500 字
3. 每 500 字安排一个金句或转折，防止读者划走
4. 结尾收拢观点 + 互动引导

用户没要求先看大纲就直接写。用户要求了，就先给 5-8 行的结构，确认后再写。

### 第 5 步：写正文

- 目标 1800-2200 字
- 严格贴住第 2 步的风格画像
- 多用具体的人、事、数字，少用形容词
- 每写完一块，回头检查一次文风有没有跑偏

### 第 6 步：自检

用 `references/writing-rules.md` 底部的检查清单逐条过。任何一条不过就改，改完再输出。

写完数一下正文的中文字符数（有命令行工具就用 `wc -m`，没有就按块估算），不在 1800-2200 之间就增删内容。

### 第 7 步：生成封面插图（油画风格）

1. 读 `references/image-prompt.md`，按公式把标题转成提示词：油画风格描述锁死，只换主体。主体从标题的意象和情绪推出来
2. 出图，优先级从高到低：① 运行 `scripts/gen-image.sh "提示词" 文件名.png`（自动读 .env 的 IMAGE_* 配置，或复用 pi 的智谱 key）② 用当前 agent 的图像生成工具。都能出图就保存为 `output/YYYY-MM-DD-slug-cover.png`，slug 与 HTML 文件名保持一致
3. 当前 agent 没有图像生成工具时：把中英双版提示词放进交付内容，说明用户可粘贴到任何生图工具（即梦、豆包、Midjourney 等），生成后按上述文件名放进 `output/`。此时 HTML 里的 {{COVER_IMAGE}} 保留占位符，并在交付说明里注明

### 第 8 步：导出 HTML（固定格式）

用 `assets/article-template.html` 生成发布用的 HTML 文件：

1. 先加载环境配置：按顺序找当前工作目录的 `.env` → skill 目录的 `.env`。固定值从里面取：ACCOUNT_NAME、FOOTER_SLOGAN、ENDING_CTA（键名见 `.env.example`）。两个都没有时，按 `.env.example` 的键问用户一次，并建议把答案写进工作目录的 `.env`。生成后也可运行 `scripts/inject-env.sh 文件名.html` 做同样的注入（适合补注入或批量处理）
2. 复制模板全文，只替换占位符：{{TITLE}}、{{DATE}}、{{WORD_COUNT}}、{{READ_MINUTES}}、{{ACCOUNT_NAME}}、{{FOOTER_SLOGAN}}、{{ENDING_QUESTION}}、{{COVER_IMAGE}}、{{BODY}}。模板的样式和结构一个字都不许改
3. {{COVER_IMAGE}} 填第 7 步的图片文件名（同目录相对路径）
4. {{BODY}} 按模板注释里的组块规则拼装：普通段落、小标题、金句、分隔符、插图（可选，每 300-500 字一张）、原话引用（转述他人观点时用，标出处）。样式固定不变
5. 保存到当前工作目录的 `output/` 下，文件名固定为 `YYYY-MM-DD-标题短slug.html`（slug 用拼音或英文短词）
6. 生成后自查：在文件里搜 `{{`，必须一个占位符都不剩。唯一例外：第 7 步走了提示词降级方案时，只允许剩 {{COVER_IMAGE}} 一个，且要在交付说明里写明
7. 交付时给出文件路径。用户在浏览器打开即可预览（封面图与 HTML 同目录才能显示），全选复制后粘贴进公众号编辑器，样式和图片会一起带过去
8. 如果所在 agent 不能写文件，就把完整 HTML 放进代码块输出，让用户自己保存为 .html 文件

### 第 9 步：给爆款建议

对照 `references/viral-techniques.md`，给 3-5 条具体建议。每条必须包含：

- 位置：第几段，或直接引用原句
- 对应的技巧：用的是清单里的哪一条
- 可直接替换的改法：不要只说"可以更好"

另外给 3 个备选标题，分别用不同技巧（数字式 / 悬念式 / 身份代入式）。

## 输出格式

按这个顺序交付：

1. 风格画像（3-5 行的浓缩版）
2. 文章标题 + 正文（末尾标注字数）
3. 封面插图：图片文件路径，或（无生图工具时）中英双版提示词
4. HTML 文件路径（output/YYYY-MM-DD-slug.html，格式由 assets/article-template.html 固定）
5. 爆款建议 + 3 个备选标题

## 维护说明

- `references/style-samples.md` 是文风锚点，用户可以随时替换成自己的文章
- `assets/article-template.html` 是固定输出模板，只换占位符不改样式。想改署名和页脚签名，直接改模板里的 {{ACCOUNT_NAME}}、{{FOOTER_SLOGAN}} 占位说明
- `references/image-prompt.md` 锁定了封面插图的油画风格，想换画风只改那里的风格描述两行
- 模板固定值（公众号名、签名、转发语）放在工作目录的 `.env`，模板见 `.env.example`；`scripts/inject-env.sh` 可对已生成的 HTML 补注入
- 样本更新后，删除 `references/style-profile.md`，下次运行会自动重新提炼
- 所有文件用相对路径引用，不依赖任何 agent 的私有功能，可直接跨 agent 复用
