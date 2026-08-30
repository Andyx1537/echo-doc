#!/bin/bash
# 定时任务实际执行的那一下。只读体检，把结果追加进日志。
# 🔴 不在这里自动清理：清理必须在 Cursor 退出的状态下做，
#    定时任务不知道你此刻在不在用，擅自动手会损坏库。

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$HOME/Library/Logs/vscdb-health.log"
mkdir -p "$(dirname "$LOG")"

{
  echo "════════ $(date '+%Y-%m-%d %H:%M:%S') ════════"
  OUT="$(/usr/bin/python3 "$HERE/vscdb-health.py" 2>&1)"
  LEVEL=$?
  echo "$OUT"
  case $LEVEL in
    0) echo "判定：健康" ;;
    1) echo "判定：该清了 —— 退出 Cursor 后跑 bash $HERE/prune-now.sh" ;;
    2) echo "判定：严重 —— 尽快退出 Cursor 跑 bash $HERE/prune-now.sh" ;;
  esac
  echo
} >> "$LOG" 2>&1

# 严重时弹一条系统通知，光写日志没人看
if [ "${LEVEL:-0}" -ge 2 ]; then
  /usr/bin/osascript -e 'display notification "Cursor 会话库过大，建议清理" with title "会话库体检"' 2>/dev/null || true
fi
