#!/bin/bash
# 在「终端 Terminal.app」里跑这个，不要在 Cursor 里跑。
#
# 为什么：清理必须在 Cursor 完全退出的状态下做（带着活连接改 SQLite 会损坏它），
# 而 Cursor 一退出，里面的 AI 助手也就没了，没人能一步步指导你。所以这个脚本
# 把全过程串成一条命令，自己检查、自己备份、自己报告，中途只问你一次要不要继续。
#
# 用法：
#   1. Cmd+Q 完全退出 Cursor
#   2. 打开「终端」（聚焦搜索 Terminal）
#   3. 粘贴这一行：
#        bash ~/Documents/workSpace/echo-doc/scripts/prune-now.sh
#   4. 跑完重新打开 Cursor
#
# 出了任何问题都能回滚：备份文件在库旁边，名字里带时间戳，改回 state.vscdb 即可。

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB="$HOME/Library/Application Support/Cursor/User/globalStorage/state.vscdb"

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }
die() { printf '\n\033[31m%s\033[0m\n\n' "$*" >&2; exit 1; }

say "第 0 步 · 检查 Cursor 是否已经退出"

[ -f "$DB" ] || die "找不到数据库：$DB"

# 🔴 只认 lsof。另外两个判据都试过、都会静默放行，别再换回去：
#   pgrep/ps —— 这台机器上直接坏掉，返回空，于是「查不到」被当成「没开着」。
#   SQLite 排他锁 —— WAL 模式下读连接不挡写事务，Cursor 开着照样拿得到。
# lsof 拿不到结果时也要拒绝，不能假设「查不出来 = 没占用」。
command -v lsof >/dev/null 2>&1 || die "找不到 lsof，没法确认数据库有没有被占用。查不出来就不动手。"

HOLDERS="$(lsof -t -- "$DB" 2>/dev/null || true)"
if [ -n "$HOLDERS" ]; then
  die "还有进程开着数据库（PID $(echo "$HOLDERS" | tr '\n' ' ')）。
  请 Cmd+Q 完全退出 Cursor——点红叉不算，要等 Dock 图标下面的小圆点消失。"
fi

printf '  Cursor 已退出，库大小 %s\n' "$(du -h "$DB" | cut -f1)"

say "第 1 步 · 先把你的输入导出存档（这一步必须成功，否则不往下走）"
python3 "$HERE/export-user-inputs.py" || die "存档失败，已停止。没有存档就不会动数据库。"

say "第 2 步 · 看看会删掉什么（只看，不动）"
python3 "$HERE/vscdb-prune.py"

say "第 3 步 · 确认"
printf '  上面列出的都是「会话索引已经不再指向」的气泡，界面上本来就看不到。\n'
printf '  被引用的一条都不会动，你能看见的历史不会少任何东西。\n'
printf '  执行前会自动备份（需要和库同样大小的磁盘空间）。\n\n'
read -r -p "  确定要清理吗？输入 yes 继续，其他任意键取消：" ANSWER

if [ "$ANSWER" != "yes" ]; then
  printf '\n  已取消，什么都没改。\n\n'
  exit 0
fi

say "第 4 步 · 执行（VACUUM 那一步很慢，可能要几分钟，别关窗口）"
python3 "$HERE/vscdb-prune.py" --apply

say "完成"
printf '  现在可以重新打开 Cursor 了。\n'
printf '  确认一切正常之后，可以删掉备份文件腾出空间：\n'
printf '    ls -la "%s".prune-backup-*\n\n' "$DB"
