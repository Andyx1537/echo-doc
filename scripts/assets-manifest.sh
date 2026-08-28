#!/usr/bin/env bash
# 重建资源清单 MANIFEST.json。往 static/ 加删物料后跑一次。
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# 2026-08-28 拆仓后资源根搬进本仓，缺省改为 $REPO_ROOT/Echo-assets。
ASSETS_DIR="${ECHO_ASSETS_DIR:-$REPO_ROOT/Echo-assets}"

[ -d "$ASSETS_DIR/static" ] || { echo "✗ 资源根不存在: $ASSETS_DIR"; exit 1; }

python3 - "$ASSETS_DIR" <<'PY'
import hashlib, json, pathlib, sys

root = pathlib.Path(sys.argv[1])
static = root / "static"

CATEGORY_NOTE = {
    "seed-covers": ("运营种子封面（共鸣厅瀑布流）", "ai-generated",
                    "内部生成，无肖像/无文字/无商标；正式上线前若换真实内容须逐条取得授权"),
    "design-ref":  ("设计参考稿（不参与运行时）", "ai-generated", "内部生成，仅供设计对齐"),
    "docs":        ("文档配图原图（仓库内为压缩缩略图）", "ai-generated", "内部生成，仅供文档说明"),
}

entries = []
for sub in sorted(p for p in static.iterdir() if p.is_dir()):
    _, source, license_note = CATEGORY_NOTE.get(sub.name, ("", "unknown", "来源待补"))
    for f in sorted(sub.rglob("*")):
        if not f.is_file() or f.name.startswith("."):
            continue
        entries.append({
            "path": str(f.relative_to(static)),
            "category": sub.name,
            "bytes": f.stat().st_size,
            "sha256": hashlib.sha256(f.read_bytes()).hexdigest()[:16],
            "source": source,
            "licenseNote": license_note,
        })

manifest = {
    "schema": 1,
    "note": "Echo 静态物料清单。校验用 scripts/assets-check.sh。"
            "用户上传物（runtime/）不入清单——含个人信息，不可分发。",
    "categories": {k: v[0] for k, v in CATEGORY_NOTE.items()},
    "totalFiles": len(entries),
    "totalBytes": sum(e["bytes"] for e in entries),
    "files": entries,
}
(root / "MANIFEST.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(f"✓ 清单已重建：{len(entries)} 个文件，{manifest['totalBytes'] / 1048576:.1f}MB")
for name in sorted({e["category"] for e in entries}):
    print(f"    {name:14s} {sum(1 for e in entries if e['category'] == name):3d} 个")
PY
