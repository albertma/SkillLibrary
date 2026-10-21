#!/usr/bin/env bash
# 安装库里的 skill 到各 agent 的 skill 目录
# 用法: ./install.sh [选项] [skill名...]
#   不带参数     列出可安装的 skills
#   --link      软链安装（仓库改动即时生效于所有 agent）
set -euo pipefail
cd "$(dirname "$0")"

MODE="copy"
args=()
for a in "$@"; do
  case "$a" in
    --link) MODE="link" ;;
    *) args+=("$a") ;;
  esac
done

TARGETS=(
  "$HOME/.agents/skills"      # Agent Skills 标准位置（workbuddy / hermes / pi 均可发现）
  "$HOME/.pi/agent/skills"    # pi agent 用户级目录
)

if [ ${#args[@]} -eq 0 ]; then
  echo "可安装的 skills:"
  for d in */; do
    [ -f "$d/SKILL.md" ] && echo "  ${d%/}"
  done
  exit 0
fi

for s in "${args[@]}"; do
  if [ ! -f "$s/SKILL.md" ]; then
    echo "跳过 $s（没有 SKILL.md）"
    continue
  fi
  for t in "${TARGETS[@]}"; do
    mkdir -p "$t"
    rm -rf "$t/$s"
    if [ "$MODE" = "link" ]; then
      ln -s "$(cd "$s" && pwd)" "$t/$s"
      echo "[软链] $t/$s -> $(cd "$s" && pwd)"
    else
      cp -r "$s" "$t/"
      echo "[复制] $t/$s"
    fi
  done
done

echo
echo "验证：pi 里执行 /skill:skill名，或让 agent「用 skill名 把这段素材写成公众号文章：……」"
