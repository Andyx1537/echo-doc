#!/usr/bin/env python3
"""把 Cursor 会话库里所有「用户输入」提取出来，落成可长期保存的存档。

为什么需要它：state.vscdb 会无限膨胀（实测 19.4 GB，其中 94% 是索引已经
不引用的无主气泡），迟早要清。但用户真正手打的内容混在里面，只有 34 MB，
占 0.25%。清库之前必须先把这 0.25% 捞干净。

🔴 两条硬规矩：
1. **只读打开数据库。** 这个脚本永远不写 state.vscdb。
2. **不丢弃任何一条。** 判定为机器生成的也照样写进 jsonl，只是不进 Markdown
   正文。判错的代价是永久丢失用户输入，而多留几条只是文件大一点。

用法：
    python3 scripts/export-user-inputs.py [输出目录]
默认输出到 docs/archive/。
"""

import glob
import json
import os
import re
import sqlite3
import sys
import datetime
from collections import defaultdict

DB = os.path.expanduser(
    "~/Library/Application Support/Cursor/User/globalStorage/state.vscdb"
)
# 第二个来源。两边互有缺失：库被摘要挤掉过消息，转录则漏收了另一批。
# 实测差集是双向的（34 / 16），所以必须两边都取再合并。
TRANSCRIPTS = os.path.expanduser(
    "~/.cursor/projects/Users-andy-Documents-workSpace/agent-transcripts"
)

# 子代理跑完后系统回灌给父线的模板提示词。它长得像用户消息，
# 但一个字都不是用户打的——只能按开头的固定英文句式认。
BOILERPLATE = (
    "The beginning of the above subagent result",
    "The following task has finished",
    "Perform any follow-up actions",
    "Perform any necessary follow-up actions",
    "Briefly inform the user about the task result",
    "The user is not aware of the above result",
)

# 系统在用户消息外面包的壳。这些不是用户打的，剥掉。
WRAPPERS = [
    "user_info", "agent_transcripts", "rules", "agent_skills",
    "available_instructions", "dynamic_tool_catalog", "system_reminder",
    "attached_files", "additional_data", "current_file", "open_files",
    "linter_errors", "recently_viewed_files", "custom_instructions",
    "user_rules", "project_layout", "attached_folders",
]


def strip_wrappers(text):
    for tag in WRAPPERS:
        text = re.sub(rf"<{tag}>.*?</{tag}>", "", text, flags=re.S)
    text = re.sub(r"<timestamp>.*?</timestamp>", "", text, flags=re.S)
    return text.strip()


def extract_human(text):
    """剥出用户真正打的字。判定为机器生成时返回 (None, 原因)。"""
    # 子代理完成通知：整条都是系统拼的，里面的 <user_query> 也是模板文案
    if "<system_notification>" in text:
        return None, "子代理完成通知"
    body = strip_wrappers(text)
    m = re.search(r"<user_query>(.*?)</user_query>", body, re.S)
    if m:
        body = m.group(1).strip()
    body = re.sub(r"<[^>]+>", "", body).strip()
    if not body:
        return None, "剥壳后为空"
    if body.startswith(BOILERPLATE):
        return None, "子代理回灌模板"
    return body, None


def fmt_time(ms):
    if not ms:
        return "时间未知"
    try:
        return datetime.datetime.fromtimestamp(ms / 1000).strftime("%Y-%m-%d %H:%M")
    except (ValueError, OSError, OverflowError):
        return "时间未知"


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "archive"
    )
    os.makedirs(out_dir, exist_ok=True)

    if not os.path.exists(DB):
        sys.exit(f"找不到数据库：{DB}")

    con = sqlite3.connect(f"file:{DB}?mode=ro&immutable=1", uri=True)
    cur = con.cursor()

    cur.execute(
        "SELECT composerId, isSubagent, subagentTypeName, createdAt, lastUpdatedAt "
        "FROM composerHeaders"
    )
    headers = {r[0]: r[1:] for r in cur.fetchall()}

    # 会话索引：用来判断一条气泡还在不在会话里。摘要会把老消息踢出索引，
    # 但气泡本身留在库里——那些「掉出去的」恰恰是最容易被误删的用户输入。
    referenced, names, order = {}, {}, {}
    cur.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
    for key, val in cur.fetchall():
        cid = key.split(":", 1)[1]
        try:
            data = json.loads(val)
        except (json.JSONDecodeError, TypeError):
            continue
        chain = data.get("fullConversationHeadersOnly") or []
        referenced[cid] = {h.get("bubbleId") for h in chain}
        order[cid] = {h.get("bubbleId"): i for i, h in enumerate(chain)}
        names[cid] = data.get("name") or ""

    # 只捞 type=1。全表 13.6 GB，按 type 过滤能把要解析的量压到 34 MB。
    cur.execute(
        "SELECT key, value FROM cursorDiskKV "
        "WHERE key LIKE 'bubbleId:%' AND value LIKE '%\"type\":1,%'"
    )
    records = []
    for key, val in cur.fetchall():
        _, cid, bid = key.split(":", 2)
        try:
            bubble = json.loads(val)
        except (json.JSONDecodeError, TypeError):
            continue
        if bubble.get("type") != 1:
            continue
        raw = (bubble.get("text") or "").strip()
        if not raw:
            continue
        is_sub, sub_type, created, updated = headers.get(cid, (0, None, None, None))
        human, reason = extract_human(raw)
        records.append({
            "conversationId": cid,
            "conversationName": names.get(cid, ""),
            "isSubagent": bool(is_sub),
            "subagentType": sub_type,
            "conversationCreatedAt": created,
            "conversationUpdatedAt": updated,
            "bubbleId": bid,
            "inIndex": bid in referenced.get(cid, set()),
            "turnIndex": order.get(cid, {}).get(bid),
            "isHuman": human is not None,
            "notHumanReason": reason,
            "text": human if human is not None else raw,
            "rawLength": len(raw),
            "images": len(bubble.get("images") or []),
        })

    # 第二遍：转录文件。会话是不是子代理，以 composerHeaders 为准；
    # 目录层级判断不了——实测子代理也有自己的顶层目录。
    for path in sorted(glob.glob(os.path.join(TRANSCRIPTS, "*", "*.jsonl"))):
        cid = os.path.basename(os.path.dirname(path))
        is_sub, sub_type, created, updated = headers.get(cid, (0, None, None, None))
        for line in open(path, encoding="utf-8"):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("role") != "user":
                continue
            parts = (obj.get("message") or {}).get("content") or []
            raw = "".join(p.get("text", "") for p in parts if isinstance(p, dict)).strip()
            if not raw:
                continue
            human, reason = extract_human(raw)
            records.append({
                "conversationId": cid,
                "conversationName": names.get(cid, ""),
                "isSubagent": bool(is_sub),
                "subagentType": sub_type,
                "conversationCreatedAt": created,
                "conversationUpdatedAt": updated,
                "bubbleId": None,
                "inIndex": True,
                "turnIndex": None,
                "isHuman": human is not None,
                "notHumanReason": reason,
                "text": human if human is not None else raw,
                "rawLength": len(raw),
                "images": 0,
                "source": "transcript",
            })

    for r in records:
        r.setdefault("source", "db")

    # 重生成会产出多条内容相同的气泡。同一会话内按正文去重，
    # 但保留「掉出索引」的那条标记——它证明这句话曾经存在过。
    seen, deduped = set(), []
    for r in sorted(records, key=lambda x: (x["conversationId"], x["turnIndex"] is None,
                                            x["turnIndex"] or 0)):
        sig = (r["conversationId"], r["text"])
        if sig in seen:
            continue
        seen.add(sig)
        deduped.append(r)

    deduped.sort(key=lambda r: (r["conversationUpdatedAt"] or 0,
                                r["turnIndex"] if r["turnIndex"] is not None else 10**9))

    with open(os.path.join(out_dir, "user-inputs.jsonl"), "w", encoding="utf-8") as f:
        for r in deduped:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    human_rows = [r for r in deduped if r["isHuman"] and not r["isSubagent"]]
    by_conv = defaultdict(list)
    for r in human_rows:
        by_conv[r["conversationId"]].append(r)
    convs = sorted(by_conv.items(), key=lambda kv: -(kv[1][0]["conversationUpdatedAt"] or 0))
    chars = sum(len(r["text"]) for r in human_rows)
    dropped_out = sum(1 for r in human_rows if not r["inIndex"])

    with open(os.path.join(out_dir, "USER-INPUTS.md"), "w", encoding="utf-8") as f:
        f.write("# 用户输入存档\n\n")
        f.write(f"> 由 `scripts/export-user-inputs.py` 自动导出，"
                f"{datetime.datetime.now():%Y-%m-%d %H:%M} 生成\n>\n")
        f.write(f"> **{len(human_rows)} 条手打输入，{chars:,} 字，{len(by_conv)} 个会话。**"
                f"其中 **{dropped_out} 条已从会话索引里掉出**"
                f"（被摘要挤掉，界面上已经看不到，只有这里还留着）。\n>\n")
        f.write("> 🔴 这份文件是清库前的保全副本。数据库可以清，这里不能丢。\n")
        f.write("> 子代理提示词与系统通知不进本文件，但都在 `user-inputs.jsonl` 里。\n\n")
        f.write("## 会话索引\n\n| 会话 | 最后活动 | 手打条数 | 掉出索引 |\n|---|---|---:|---:|\n")
        for cid, rows in convs:
            name = (rows[0]["conversationName"] or "(未命名)")[:40]
            lost = sum(1 for r in rows if not r["inIndex"])
            f.write(f"| {name} `{cid[:8]}` | {fmt_time(rows[0]['conversationUpdatedAt'])} "
                    f"| {len(rows)} | {lost or ''} |\n")
        f.write("\n---\n")
        for cid, rows in convs:
            name = rows[0]["conversationName"] or "(未命名)"
            f.write(f"\n## {name}\n\n`{cid}` · {fmt_time(rows[0]['conversationUpdatedAt'])}"
                    f" · {len(rows)} 条\n\n")
            for r in rows:
                mark = "" if r["inIndex"] else " · 🔴 已掉出索引"
                pos = f"#{r['turnIndex']}" if r["turnIndex"] is not None else "位置不详"
                img = f" · {r['images']} 张图" if r["images"] else ""
                f.write(f"### {pos}{img}{mark}\n\n")
                for line in r["text"].split("\n"):
                    f.write(f"> {line}\n")
                f.write("\n")

    print(f"用户气泡         : {len(records):,} 条 → 去重后 {len(deduped):,} 条")
    print(f"手打输入（主对话）: {len(human_rows):,} 条，{chars:,} 字，{len(by_conv)} 个会话")
    print(f"  其中已掉出索引 : {dropped_out:,} 条")
    print(f"子代理提示词     : {sum(1 for r in deduped if r['isSubagent']):,} 条（只进 jsonl）")
    print(f"机器生成通知     : {sum(1 for r in deduped if not r['isHuman']):,} 条（只进 jsonl）")
    print(f"输出目录         : {out_dir}")


if __name__ == "__main__":
    main()
