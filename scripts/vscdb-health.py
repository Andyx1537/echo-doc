#!/usr/bin/env python3
"""Cursor 会话库体检。只读，不改任何东西。

背景：state.vscdb 没有垃圾回收。每次重新生成、重试、编辑都会写新气泡，
旧气泡从会话索引里掉出去之后仍然留在库里，永远不删。实测跑到 19.4 GB 时，
94% 是这种无主气泡，全表扫一次要 50 秒——UI 启动时读代理状态会因此卡住，
把已经结束的会话渲染成一直转圈的「working」。

用法：
    python3 scripts/vscdb-health.py            # 体检
    python3 scripts/vscdb-health.py --json     # 机器可读，给定时任务用

退出码：0 健康 / 1 该清了 / 2 严重
"""

import json
import os
import sqlite3
import sys

DB = os.path.expanduser(
    "~/Library/Application Support/Cursor/User/globalStorage/state.vscdb"
)
GB = 1024 ** 3

# 阈值。8 GB 是经验值：实测 19 GB 时全表扫描 50 秒、UI 明显出问题；
# 留一半余量报警，才来得及在出问题之前清。
WARN_BYTES = 8 * GB
CRIT_BYTES = 15 * GB
WARN_ORPHAN_RATIO = 0.60


def collect():
    if not os.path.exists(DB):
        sys.exit(f"找不到数据库：{DB}")
    size = os.path.getsize(DB)
    con = sqlite3.connect(f"file:{DB}?mode=ro&immutable=1", uri=True)
    cur = con.cursor()

    referenced = set()
    conversations = 0
    cur.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
    for (val,) in cur.fetchall():
        try:
            data = json.loads(val)
        except (json.JSONDecodeError, TypeError):
            continue
        conversations += 1
        for h in data.get("fullConversationHeadersOnly") or []:
            referenced.add(h.get("bubbleId"))

    total_n = total_b = orphan_n = orphan_b = 0
    cur.execute("SELECT key, length(value) FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
    for key, blen in cur.fetchall():
        blen = blen or 0
        total_n += 1
        total_b += blen
        if key.rsplit(":", 1)[1] not in referenced:
            orphan_n += 1
            orphan_b += blen

    cur.execute("SELECT COUNT(*), SUM(length(value)) FROM cursorDiskKV WHERE key LIKE 'agentKv:%'")
    kv_n, kv_b = cur.fetchone()

    return {
        "fileBytes": size,
        "conversations": conversations,
        "bubbles": total_n,
        "bubbleBytes": total_b,
        "orphanBubbles": orphan_n,
        "orphanBytes": orphan_b,
        "orphanRatio": (orphan_b / total_b) if total_b else 0.0,
        "agentKv": kv_n,
        "agentKvBytes": kv_b or 0,
    }


def main():
    s = collect()
    level = 0
    if s["fileBytes"] >= CRIT_BYTES:
        level = 2
    elif s["fileBytes"] >= WARN_BYTES or s["orphanRatio"] >= WARN_ORPHAN_RATIO:
        level = 1

    if "--json" in sys.argv:
        s["level"] = level
        print(json.dumps(s, ensure_ascii=False))
        return level

    tag = {0: "健康", 1: "该清了", 2: "严重"}[level]
    print(f"库文件      : {s['fileBytes']/GB:.2f} GB   [{tag}]")
    print(f"会话        : {s['conversations']:,}")
    print(f"气泡        : {s['bubbles']:,} 条，{s['bubbleBytes']/GB:.2f} GB")
    print(f"  其中无主  : {s['orphanBubbles']:,} 条，{s['orphanBytes']/GB:.2f} GB"
          f"（{s['orphanRatio']*100:.0f}%）  <- 会话索引已经不指向它们")
    print(f"agentKv     : {s['agentKv']:,} 条，{s['agentKvBytes']/GB:.2f} GB")
    if level:
        print(f"\n可回收约 {s['orphanBytes']/GB:.2f} GB。清理前先跑："
              f"\n  python3 scripts/export-user-inputs.py"
              f"\n然后完全退出 Cursor，再跑："
              f"\n  python3 scripts/vscdb-prune.py --apply")
    return level


if __name__ == "__main__":
    sys.exit(main())
