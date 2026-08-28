#!/usr/bin/env bash
# 校验各仓的 .proto 副本与本仓真源一致。不一致退 1。
#
# 为什么需要这个脚本
# ------------------
# 产品负责人 2026-08-28 裁定：.proto 真源放在 echo-doc 仓的 proto/，各消费仓保留副本。
# 这个安排唯一的风险是「两份不一致时不会有任何报错」——后端照旧编译、照旧通过，
# 只是编出来的协议和真源对不上。本脚本就是把那个静默失效变成一个非零退出码。
#
# 用法
#   scripts/proto-check.sh                    # 自动找同级的 echo/ 仓
#   scripts/proto-check.sh /path/to/echo      # 指定消费仓根目录
#   scripts/proto-check.sh --fix /path/to/echo  # 用真源覆盖副本（只允许这个方向）
#
# 消费仓与其副本目录的对应写在下面 CONSUMERS 里，新增消费仓时在那里加一行。
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TRUTH="$REPO_ROOT/proto"

# 消费仓名 → 该仓内副本目录的相对路径
declare -a CONSUMERS=(
  "echo:echo-server/src/main/proto"
)

FIX=0
if [ "${1:-}" = "--fix" ]; then FIX=1; shift; fi
TARGET="${1:-}"

if [ ! -d "$TRUTH" ]; then
  echo "✗ 真源目录不存在: $TRUTH"
  exit 1
fi

fail=0

for entry in "${CONSUMERS[@]}"; do
  name="${entry%%:*}"
  rel="${entry#*:}"

  if [ -n "$TARGET" ]; then
    repo="$TARGET"
  else
    repo="$(cd "$REPO_ROOT/.." && pwd)/$name"
  fi

  copy="$repo/$rel"

  if [ ! -d "$copy" ]; then
    echo "— 跳过 $name：副本目录不在 $copy"
    echo "  （不算失败，但也就意味着这一轮没有校验到它。要校验请传路径。）"
    continue
  fi

  echo "校验 $name: $copy"

  # 先比文件集合，再比内容——只比内容会漏掉「真源新增了一个文件而副本没有」
  truth_list="$(cd "$TRUTH" && ls -1 *.proto 2>/dev/null | sort)"
  copy_list="$(cd "$copy" && ls -1 *.proto 2>/dev/null | sort)"

  if [ "$truth_list" != "$copy_list" ]; then
    echo "  ✗ 文件集合不一致："
    diff <(echo "$truth_list") <(echo "$copy_list") | sed 's/^/      /' || true
    fail=1
  fi

  while IFS= read -r f; do
    [ -z "$f" ] && continue
    [ -f "$copy/$f" ] || continue
    a="$(shasum -a 256 "$TRUTH/$f" | cut -d' ' -f1)"
    b="$(shasum -a 256 "$copy/$f" | cut -d' ' -f1)"
    if [ "$a" != "$b" ]; then
      echo "  ✗ 内容不一致: $f"
      fail=1
    fi
  done <<< "$truth_list"

  if [ "$fail" -ne 0 ] && [ "$FIX" -eq 1 ]; then
    echo "  → --fix：用真源覆盖 $copy"
    rm -f "$copy"/*.proto
    cp "$TRUTH"/*.proto "$copy"/
    echo "  ✓ 已同步。记得在 $name 仓里提交这次改动。"
    fail=0
  fi
done

if [ "$fail" -ne 0 ]; then
  cat <<'EOF'

✗ 协议副本与真源不一致。

  真源是 echo-doc 仓的 proto/，方向只有一个：先改真源，再同步到消费仓。
  反过来改副本再往回抄，迟早会把两边都改乱。

  同步：scripts/proto-check.sh --fix /path/to/消费仓
EOF
  exit 1
fi

echo "✓ 所有已定位到的副本与真源一致"
