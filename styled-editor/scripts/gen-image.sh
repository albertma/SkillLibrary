#!/usr/bin/env bash
# 生成油画插图：调用 OpenAI 兼容的 images/generations 接口（默认智谱 CogView 免费档）
# 用法: gen-image.sh "提示词" 输出文件.png [尺寸]
# 尺寸默认 1152x864（3:2）；CogView 支持 1024x1024/768x1344/864x1152/1344x768/1152x864/1440x720/720x1440
# 配置(.env 或环境变量): IMAGE_API_KEY / IMAGE_API_URL / IMAGE_MODEL
set -euo pipefail

prompt="${1:?用法: gen-image.sh \"提示词\" 输出文件.png [尺寸]}"
out="${2:?缺少输出文件名}"
size="${3:-1152x864}"

# 加载 .env：先工作目录，再 skill 目录
for f in ./.env "$(dirname "$0")/../.env"; do
  if [ -f "$f" ]; then set -a; . "$f"; set +a; break; fi
done

: "${IMAGE_API_URL:=https://open.bigmodel.cn/api/paas/v4/images/generations}"
: "${IMAGE_MODEL:=cogview-3-flash}"

# 没配 IMAGE_API_KEY 时，尝试从 pi 的 models.json 里取智谱 key
if [ -z "${IMAGE_API_KEY:-}" ]; then
  mj="$HOME/.pi/agent/models.json"
  if [ -f "$mj" ]; then
    IMAGE_API_KEY=$(python3 -c "
import json
try:
    d = json.load(open('$mj'))
    print(d['providers']['cc-switch-zhipu-glm']['apiKey'])
except Exception:
    pass")
  fi
fi
[ -n "${IMAGE_API_KEY:-}" ] || { echo "缺少 IMAGE_API_KEY：在 .env 配置，或在 ~/.pi/agent/models.json 配智谱 provider"; exit 1; }

payload=$(python3 - "$prompt" "$size" "$IMAGE_MODEL" << 'PY'
import json, sys
print(json.dumps({"model": sys.argv[3], "prompt": sys.argv[1], "size": sys.argv[2]}, ensure_ascii=False))
PY
)

resp=$(curl -s --max-time 180 "$IMAGE_API_URL" \
  -H "Authorization: Bearer $IMAGE_API_KEY" -H "Content-Type: application/json" \
  -d "$payload")

url=$(python3 - "$resp" << 'PY'
import json, sys
try:
    d = json.loads(sys.argv[1])
    print(d["data"][0].get("url") or d["data"][0].get("b64_json", ""))
except Exception:
    print("")
PY
)
if [ -z "$url" ]; then echo "生成失败：$(echo "$resp" | head -c 300)"; exit 1; fi

# 返回 url 或 b64 都能存
case "$url" in
  http*) curl -s --max-time 180 -o "$out" "$url" ;;
  *) echo "$url" | base64 -d > "$out" ;;
esac

echo "已生成: $out ($(du -h "$out" | cut -f1), ${size}, ${IMAGE_MODEL})"
