#!/usr/bin/env python3
"""清掉 Cursor 会话库里的无主气泡。

只删「会话索引不再引用」的气泡。这类气泡在界面上已经完全看不到了——
它们是重新生成、重试、摘要挤压留下的残骸，Cursor 自己没有回收机制。
被索引引用的一条都不动，所以界面上看得见的历史不会少任何东西。

🔴 三道闸门，缺一不可：
1. **必须先跑 export-user-inputs.py**，且存档文件存在。脚本会自己检查。
2. **必须完全退出 Cursor。** 检测到 -wal 有内容就拒绝执行——带着活连接改库会损坏它。
3. **默认干跑。** 不加 --apply 只报告要删什么，不动一个字节。

用法：
    python3 scripts/vscdb-prune.py             # 干跑，只看会删多少
    python3 scripts/vscdb-prune.py --apply     # 真删（先自动备份）

回滚：备份在同目录 state.vscdb.prune-backup-<时间戳>，
把它改回 state.vscdb 即可。
"""

import json
import os
import shutil
import sqlite3
import sys
import time

DB = os.path.expanduser(
    "~/Library/Application Support/Cursor/User/globalStorage/state.vscdb"
)
ARCHIVE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docs", "archive", "user-inputs.jsonl",
)
GB = 1024 ** 3


def preflight(apply):
    if not os.path.exists(DB):
        sys.exit(f"找不到数据库：{DB}")

    if not os.path.exists(ARCHIVE):
        sys.exit("拒绝执行：还没有用户输入存档。\n"
                 "  先跑 python3 scripts/export-user-inputs.py")
    age_h = (time.time() - os.path.getmtime(ARCHIVE)) / 3600
    n = sum(1 for _ in open(ARCHIVE, encoding="utf-8"))
    print(f"存档：{n:,} 条，{age_h:.1f} 小时前生成")
    if age_h > 24:
        sys.exit("拒绝执行：存档超过 24 小时，可能漏掉了这期间的输入。请重新导出。")

    wal = DB + "-wal"
    if apply and os.path.exists(wal) and os.path.getsize(wal) > 0:
        sys.exit(f"拒绝执行：{os.path.basename(wal)} 还有 "
                 f"{os.path.getsize(wal)/1048576:.1f} MB 未落盘，说明 Cursor 还开着。\n"
                 "  请完全退出 Cursor（Cmd+Q）后重试。")


def main():
    apply = "--apply" in sys.argv
    preflight(apply)

    mode = "" if apply else "?mode=ro&immutable=1"
    con = sqlite3.connect(f"file:{DB}{mode}", uri=True)
    cur = con.cursor()

    referenced = set()
    cur.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
    for (val,) in cur.fetchall():
        try:
            data = json.loads(val)
        except (json.JSONDecodeError, TypeError):
            continue
        for h in data.get("fullConversationHeadersOnly") or []:
            referenced.add(h.get("bubbleId"))
    print(f"会话索引引用了 {len(referenced):,} 个气泡")

    victims, freed = [], 0
    cur.execute("SELECT key, length(value) FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
    for key, blen in cur.fetchall():
        if key.rsplit(":", 1)[1] not in referenced:
            victims.append(key)
            freed += blen or 0
    print(f"无主气泡 {len(victims):,} 条，占 {freed/GB:.2f} GB")

    if not apply:
        print("\n干跑，没有改动任何东西。确认无误后加 --apply 执行。")
        return

    backup = f"{DB}.prune-backup-{time.strftime('%Y%m%d-%H%M%S')}"
    print(f"\n备份到 {os.path.basename(backup)} …")
    shutil.copy2(DB, backup)

    print(f"删除 {len(victims):,} 条 …")
    for i in range(0, len(victims), 500):
        cur.executemany("DELETE FROM cursorDiskKV WHERE key=?",
                        [(k,) for k in victims[i:i + 500]])
        con.commit()

    before = os.path.getsize(DB)
    print("VACUUM 回收空间（这一步很慢，别中断）…")
    con.execute("VACUUM")
    con.close()
    after = os.path.getsize(DB)
    print(f"\n完成：{before/GB:.2f} GB → {after/GB:.2f} GB，回收 {(before-after)/GB:.2f} GB")
    print(f"回滚：把 {os.path.basename(backup)} 改名回 state.vscdb")


if __name__ == "__main__":
    main()
