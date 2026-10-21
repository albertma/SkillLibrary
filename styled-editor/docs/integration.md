# 对接 workbuddy / pi agent / hermes agent

这个 skill 按 Agent Skills 规范（agentskills.io）写成：一个目录，`SKILL.md` 带标准 frontmatter，所有引用都是目录内相对路径，不含任何 agent 私有语法。因此同一份文件可以直接被多个 agent 复用，不需要改动。

## 通用装法（推荐）

装到 Agent Skills 标准用户目录 `~/.agents/skills/`，所有支持该规范的 agent 都能发现：

```bash
./install.sh          # 复制安装
./install.sh --link   # 软链安装（多 agent 共享同一份文件，改一处处处生效）
```

## pi agent

pi 原生支持 Agent Skills，以下位置任选其一：

- `~/.pi/agent/skills/styled-editor/`（用户级，全局可用）
- 项目下 `.pi/skills/styled-editor/`（项目级）
- `~/.agents/skills/styled-editor/`（Agent Skills 标准位置）
- 项目下 `.agents/skills/styled-editor/`（从工作目录向上自动发现）

使用方式：

- 自动触发：直接丢素材，比如"把这个大纲写成公众号文章"
- 强制触发：`/skill:styled-editor 这是我的大纲：……`
- 修改 skill 文件后，在会话里执行 `/reload` 重新加载

## workbuddy

- 如果 workbuddy 支持 Agent Skills 标准位置（`~/.agents/skills/`），装好即用
- 如果它有自己的 skill 目录或注册配置，把 `styled-editor/` 整个目录复制或软链过去即可。skill 内部没有 pi 专属语法，不需要改任何内容

## hermes agent

同上：

- 优先装到 `~/.agents/skills/styled-editor/`
- 若 hermes 有独立的 skill 配置项（例如在配置文件里声明 skill 路径），把本目录注册进去

## 验证是否生效

装好后发送这句话测试：

> 用 styled-editor 把这段素材写成公众号文章：我今天在地铁上看到……

正常响应顺序：先给 3-5 行风格画像，再给 1800-2200 字正文，然后给油画风格的封面插图（图片文件或提示词）和 `output/` 目录下的 HTML 文件（格式固定，浏览器可直接预览），最后给爆款建议和 3 个备选标题。如果直接开写、没有风格画像，说明 skill 没被加载，检查安装位置。

## 多 agent 共享文风

各 agent 读的是各自安装目录里的副本。想让所有 agent 用同一份最新文风，用软链代替复制：

```bash
ln -sfn /path/to/styled_editor/styled-editor ~/.agents/skills/styled-editor
ln -sfn /path/to/styled_editor/styled-editor ~/.pi/agent/skills/styled-editor
```

之后改一处 `references/style-samples.md`，所有 agent 同时生效。
