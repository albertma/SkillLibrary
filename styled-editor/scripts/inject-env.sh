#!/usr/bin/env bash
# 把 .env 里的固定值注入已生成的 HTML（替换 {{ACCOUNT_NAME}} 等占位符）
# 用法: inject-env.sh <html文件> [env文件]
# env 文件缺省时按顺序找: ./.env → skill 目录下的 .env
set -euo pipefail

file="${1:?用法: inject-env.sh <html文件> [env文件]}"
[ -f "$file" ] || { echo "文件不存在: $file"; exit 1; }

env_file="${2:-}"
if [ -z "$env_file" ]; then
  if [ -f .env ]; then
    env_file=".env"
  else
    env_file="$(cd "$(dirname "$0")/.." && pwd)/.env"
  fi
fi
[ -f "$env_file" ] || { echo "找不到 .env（找过 ./ 和 skill 目录）。可先执行: cp styled-editor/.env.example .env"; exit 1; }

python3 - "$file" "$env_file" << 'PY'
import sys, re, pathlib

html_path, env_path = sys.argv[1], sys.argv[2]
text = pathlib.Path(html_path).read_text(encoding="utf-8")

env = {}
for line in pathlib.Path(env_path).read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    env[k.strip()] = v.strip().strip('"').strip("'")

replaced = [k for k, v in env.items() if "{{" + k + "}}" in text]
for k, v in env.items():
    text = text.replace("{{" + k + "}}", v)

pathlib.Path(html_path).write_text(text, encoding="utf-8")
print("env 来源:", env_path)
print("已注入键:", ", ".join(replaced) if replaced else "(无匹配占位符)")
left = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", text)))
print("残留占位符:", ", ".join(left) if left else "无")
PY
