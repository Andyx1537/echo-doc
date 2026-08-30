#!/bin/bash
# 装/卸「会话库定时体检」。只读，不会自动清理任何东西。
#
# 为什么要定时：state.vscdb 没有垃圾回收，跑到 18 GB 才被发现，那时全表扫一次
# 要 50 秒、UI 读代理状态会卡住，把已结束的会话渲染成一直转圈的 working。
# 定时体检的意义是在它长到那么大**之前**就叫一声。
#
# 用法：
#   bash scripts/install-health-timer.sh            # 安装（每天 10:00 跑一次）
#   bash scripts/install-health-timer.sh --status   # 看状态与最近一次结果
#   bash scripts/install-health-timer.sh --run      # 立刻跑一次
#   bash scripts/install-health-timer.sh --uninstall

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LABEL="com.echo.vscdb-health"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG="$HOME/Library/Logs/vscdb-health.log"
RUNNER="$HERE/health-run.sh"

case "${1:-install}" in
  --uninstall)
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || launchctl unload "$PLIST" 2>/dev/null || true
    rm -f "$PLIST"
    echo "已卸载。日志保留在 $LOG"
    exit 0
    ;;
  --status)
    echo "任务：$(launchctl list | grep -F "$LABEL" || echo '未安装')"
    echo "配置：$PLIST"
    echo "日志：$LOG"
    if [ -f "$LOG" ]; then echo; echo "--- 最近 20 行 ---"; tail -20 "$LOG"; fi
    exit 0
    ;;
  --run)
    bash "$RUNNER"; tail -8 "$LOG"; exit 0
    ;;
esac

mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"

cat > "$PLIST" <<PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$RUNNER</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>10</integer><key>Minute</key><integer>0</integer></dict>
  <!-- 合盖错过的补跑一次，否则笔记本永远轮不到 10 点整开着 -->
  <key>RunAtLoad</key><false/>
  <key>StandardErrorPath</key><string>$LOG</string>
</dict>
</plist>
PLISTEOF

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"

echo "已安装：每天 10:00 体检一次（只读）"
echo "  配置 $PLIST"
echo "  日志 $LOG"
echo
echo "立刻跑一次看看："
bash "$RUNNER"
tail -12 "$LOG"
