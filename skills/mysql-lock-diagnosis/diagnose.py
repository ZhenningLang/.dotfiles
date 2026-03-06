"""MySQL 锁等待诊断 — 一键输出所有排查信息。

用法:
    uv run python /Users/zhenninglang/.factory/skills/mysql-lock-diagnosis/diagnose.py --env .env.prod
    uv run python /Users/zhenninglang/.factory/skills/mysql-lock-diagnosis/diagnose.py --env .env.prod --table forge_creator_audience
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="MySQL 锁等待诊断")
    parser.add_argument("--env", required=True, help="dotenv 配置文件路径 (如 .env.prod)")
    parser.add_argument("--table", default="", help="过滤目标表名 (可选)")
    args = parser.parse_args()

    try:
        from shared.db import get_connection
    except ImportError:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
        from shared.db import get_connection

    with get_connection(dotenv_path=args.env) as conn:
        cur = conn.cursor()

        # 1. 活跃/僵尸事务
        print("=" * 60)
        print("1. innodb_trx — 活跃事务 (重点看 rows_locked > 0 的)")
        print("=" * 60)
        cur.execute(
            "SELECT trx_id, trx_state, trx_started, trx_mysql_thread_id, "
            "trx_rows_locked, trx_lock_structs, "
            "SUBSTRING(trx_query, 1, 200) AS trx_query "
            "FROM information_schema.innodb_trx "
            "ORDER BY trx_started"
        )
        trx_rows = cur.fetchall()
        suspects = []
        if not trx_rows:
            print("  (无活跃事务)")
        for r in trx_rows:
            flag = ""
            if r["trx_rows_locked"] and r["trx_rows_locked"] > 0:
                if r["trx_query"] is None and r["trx_state"] == "RUNNING":
                    flag = " *** 僵尸事务 ***"
                    suspects.append(r["trx_mysql_thread_id"])
                elif r["trx_state"] == "LOCK WAIT":
                    flag = " (被阻塞)"
                else:
                    flag = " (持有锁)"
            print(f"  trx={r['trx_id']} thread={r['trx_mysql_thread_id']} "
                  f"state={r['trx_state']} started={r['trx_started']} "
                  f"rows_locked={r['trx_rows_locked']}{flag}")
            if r["trx_query"]:
                print(f"    query: {r['trx_query']}")
        print()

        # 2. PROCESSLIST — 活跃查询和长连接
        print("=" * 60)
        print("2. PROCESSLIST — executing 查询 + 长 Sleep 连接")
        print("=" * 60)
        cur.execute("SHOW FULL PROCESSLIST")
        procs = cur.fetchall()
        table_filter = args.table.lower()
        for r in procs:
            info = (r.get("Info") or "")
            state = r.get("State") or ""
            t = r.get("Time", 0) or 0
            show = False
            if state == "executing" or "Waiting for" in state:
                show = True
            if r["Command"] == "Sleep" and t > 60:
                show = True
            if r["Id"] in suspects:
                show = True
            if table_filter and table_filter in info.lower():
                show = True
            if show:
                marker = ""
                if r["Id"] in suspects:
                    marker = " *** 僵尸事务连接 ***"
                print(f"  ID={r['Id']} User={r['User']} "
                      f"Cmd={r['Command']} Time={t}s "
                      f"State={state}{marker}")
                if info:
                    print(f"    SQL: {info[:300]}")
        print()

        # 3. INNODB STATUS — 死锁和事务摘要
        print("=" * 60)
        print("3. INNODB STATUS — 死锁记录")
        print("=" * 60)
        cur.execute("SHOW ENGINE INNODB STATUS")
        status_text = list(cur.fetchone().values())[2]

        dl_start = status_text.find("LATEST DETECTED DEADLOCK")
        if dl_start >= 0:
            dl_end = status_text.find("---", dl_start + 30)
            if dl_end < 0:
                dl_end = dl_start + 3000
            print(status_text[dl_start:dl_end][:2000])
        else:
            print("  (无死锁记录)")
        print()

        # 4. 尝试 performance_schema
        print("=" * 60)
        print("4. performance_schema.data_lock_waits (可能无权限)")
        print("=" * 60)
        try:
            cur.execute(
                "SELECT REQUESTING_ENGINE_LOCK_ID, BLOCKING_ENGINE_LOCK_ID, "
                "REQUESTING_THREAD_ID, BLOCKING_THREAD_ID "
                "FROM performance_schema.data_lock_waits LIMIT 10"
            )
            lock_waits = cur.fetchall()
            if not lock_waits:
                print("  (无锁等待)")
            for r in lock_waits:
                print(f"  requesting_thread={r['REQUESTING_THREAD_ID']} "
                      f"blocking_thread={r['BLOCKING_THREAD_ID']}")
        except Exception as e:
            print(f"  无权限: {e}")
        print()

        # 5. 总结
        if suspects:
            print("=" * 60)
            print("建议操作")
            print("=" * 60)
            for tid in suspects:
                print(f"  KILL {tid};  -- 僵尸事务，确认后执行")
            print()
            print("  执行前请确认 thread_id 对应的不是关键业务连接。")


if __name__ == "__main__":
    main()
