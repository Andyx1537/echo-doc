#!/usr/bin/env bash
# 校验资源根是否就位：目录存在、清单对得上、没有缺文件。
# 新克隆工程后先跑这个，能直接说清楚封面为什么裂开。
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# 2026-08-28 拆仓后资源根搬进本仓（原先在仓库外的同级目录），故缺省是 $REPO_ROOT/Echo-assets。
# 注意 runtime/uploads 仍在仓外：那是用户上传，受 PIPL 约束不得入库，见 Echo-assets/README.md。
ASSETS_DIR="${ECHO_ASSETS_DIR:-$REPO_ROOT/Echo-assets}"

echo "资源根: $ASSETS_DIR"

if [ ! -d "$ASSETS_DIR" ]; then
  cat <<EOF

✗ 资源根不存在。

  static/ 部分随本仓入库，正常克隆下来就该有。走到这里说明：
    1. 你在别的仓里跑这个脚本 → 请在 echo-doc 仓根目录跑
    2. 资源根在别处 → export ECHO_ASSETS_DIR=/你的/绝对路径

  目录规范见 docs/ASSETS.md
EOF
  exit 1
fi

if [ ! -f "$ASSETS_DIR/MANIFEST.json" ]; then
  echo "✗ 缺少 MANIFEST.json，无法校验完整性。跑 scripts/assets-manifest.sh 重建。"
  exit 1
fi

python3 - "$ASSETS_DIR" <<'PY'
import json, pathlib, sys

root = pathlib.Path(sys.argv[1])
manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
static = root / "static"

missing, resized = [], []
for entry in manifest["files"]:
    f = static / entry["path"]
    if not f.is_file():
        missing.append(entry["path"])
    elif f.stat().st_size != entry["bytes"]:
        resized.append(entry["path"])

total = manifest["totalFiles"]
if missing:
    print(f"\n✗ 缺失 {len(missing)}/{total} 个文件：")
    for p in missing[:10]:
        print(f"    {p}")
    if len(missing) > 10:
        print(f"    ... 另有 {len(missing) - 10} 个")
if resized:
    print(f"\n! {len(resized)} 个文件大小与清单不符（被替换过？）：")
    for p in resized[:10]:
        print(f"    {p}")

if not missing and not resized:
    print(f"✓ {total} 个静态物料齐全（{manifest['totalBytes'] / 1048576:.1f}MB）")

runtime = root / "runtime" / "uploads"
n = len(list(runtime.iterdir())) if runtime.is_dir() else 0
print(f"  runtime/uploads: {n} 项（用户上传，不校验、不分发）")

sys.exit(1 if missing else 0)
PY
