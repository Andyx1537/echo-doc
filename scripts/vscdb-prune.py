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


def assert_db_free():
    """确认没有任何进程正开着这个库。查不出来就拒绝执行，不做乐观假设。

    🔴 两个试过但不管用的判据，别再回头用：
    - `pgrep` / `ps`：这台机器上直接坏掉（sysmond service not found），返回空。
      「查不到进程」于是被当成「已经退出」，闸门静默放行。
    - SQLite 排他锁：WAL 模式下读连接不阻塞写事务，Cursor 开着照样能拿到锁。
      实测两次都放行了。

    lsof 是唯一真的能看到句柄的。所以它失败时必须**拒绝**而不是跳过——
    宁可让人多确认一次，也不能在拿不准的情况下去改一个 19 GB 的库。
    """
    import subprocess
    try:
        out = subprocess.run(["lsof", "-t", "--", DB],
                             capture_output=True, text=True, timeout=30)
    except (FileNotFoundError, OSError, subprocess.SubprocessError) as e:
        sys.exit(f"拒绝执行：没法确认数据库有没有被占用（lsof 不可用：{e}）。\n"
                 "  查不出来就不动手。请确认 Cursor 已完全退出后手动核实：\n"
                 f'    lsof -- "{DB}"')

    pids = [p for p in out.stdout.split() if p.strip()]
    if pids:
        sys.exit(f"拒绝执行：还有 {len(pids)} 个进程开着数据库（PID {', '.join(pids)}）。\n"
                 "  请 Cmd+Q 完全退出 Cursor——点红叉不算，要等 Dock 图标下的小圆点消失。")


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

    if apply:
        assert_db_free()


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
