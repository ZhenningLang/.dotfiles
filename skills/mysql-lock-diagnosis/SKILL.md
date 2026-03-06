---
name: mysql-lock-diagnosis
description: |
  排查 MySQL "Lock wait timeout exceeded" 错误。当遇到锁等待超时、死锁、
  事务阻塞等问题时使用。按优先级逐步定位阻塞源并提供修复建议。
---

# MySQL Lock Wait Timeout 排查

当遇到 `Lock wait timeout exceeded; try restarting transaction` 时，按以下流程排查。

## 前置条件

- 能连接到目标 MySQL 实例（直连或 SSH 隧道）
- 有 `information_schema` 查询权限
- 了解报错的 SQL 语句和目标表名

## 排查流程

按优先级从高到低执行。大多数情况在步骤 1-2 就能定位根因。

### Step 1: 查 innodb_trx — 找僵尸事务（最常见根因）

```sql
SELECT trx_id, trx_state, trx_started, trx_mysql_thread_id,
       trx_rows_locked, trx_lock_structs, trx_query
FROM information_schema.innodb_trx
WHERE trx_rows_locked > 0 OR trx_state != 'RUNNING'
ORDER BY trx_started;
```

**关键判断：**

| 特征 | 含义 |
|------|------|
| `trx_state = 'LOCK WAIT'` | 这是被阻塞的事务（你的写入） |
| `trx_state = 'RUNNING'` + `trx_query = NULL` + `trx_rows_locked > 0` | **僵尸事务** — 程序崩溃/超时后连接未断开，事务没 commit/rollback，但仍持有行锁 |
| `trx_started` 时间很早（几十分钟甚至几小时前） | 确认是僵尸事务 |

**僵尸事务是最常见的根因**。典型场景：Python 脚本写数据时报错退出，但 SSH 隧道保持连接，MySQL 服务端的事务没回滚。

### Step 2: 查 PROCESSLIST — 找长查询和阻塞连接

```sql
SHOW FULL PROCESSLIST;
```

或过滤关键信息：

```sql
SELECT Id, User, Host, db, Command, Time, State,
       SUBSTRING(Info, 1, 200) AS Info
FROM information_schema.processlist
WHERE Command != 'Sleep' OR Time > 60
ORDER BY Time DESC;
```

**关键判断：**

| 特征 | 含义 |
|------|------|
| `Command = 'Query'` + `State = 'executing'` + `Time` 很大 | 长时间运行的查询，可能阻塞写入 |
| `Command = 'Sleep'` + `Time` 很大 | 空闲连接，结合 Step 1 看是否持有未提交事务 |
| 同一 `Host` 出现大量连接 | 连接池泄漏 |

用 Step 1 的 `trx_mysql_thread_id` 关联 PROCESSLIST 的 `Id`，定位阻塞源的具体连接。

### Step 3: KILL 阻塞源

确认阻塞源后，KILL 对应的 MySQL 线程（**需人工确认**）：

```sql
KILL <thread_id>;
```

注意：
- KILL 会回滚该连接上未提交的事务，释放所有锁
- 不要盲目 KILL，先确认 thread_id 对应的是僵尸事务或可中断的查询
- 如果是线上业务连接，先评估影响

### Step 4: 查 INNODB STATUS — 看死锁和详细锁信息

```sql
SHOW ENGINE INNODB STATUS;
```

关注以下段落：
- `LATEST DETECTED DEADLOCK` — 最近的死锁详情（两个事务互相等待）
- `TRANSACTIONS` — 所有活跃事务及锁信息
- `SEMAPHORES` — 内部锁竞争（极少见）

### Step 5: 尝试 performance_schema（需权限）

如果有权限，可以精确查看锁等待关系：

```sql
-- MySQL 8.0+
SELECT * FROM performance_schema.data_lock_waits;
SELECT * FROM performance_schema.data_locks;
SELECT * FROM performance_schema.metadata_locks
WHERE OBJECT_NAME LIKE '%目标表名%';
```

> 阿里云 RDS 的普通用户通常无权查 performance_schema，会报 `SELECT command denied`。此时依赖 Step 1-2 即可。

## 常见根因及修复

### 1. 僵尸事务（最常见）

**现象**：`innodb_trx` 中有 `RUNNING` + `query=NULL` + `rows_locked > 0` 的事务

**根因**：程序异常退出但数据库连接未正确关闭（SSH 隧道保持连接）

**修复**：
1. KILL 僵尸连接
2. 代码中确保 connection close 前先 rollback：
```python
# Python pymysql
@contextmanager
def get_connection():
    conn = pymysql.connect(...)
    try:
        yield conn
    finally:
        try:
            conn.rollback()  # 确保异常时回滚
        except Exception:
            pass
        conn.close()
```

### 2. 长查询阻塞写入

**现象**：PROCESSLIST 中有 `executing` 状态的大查询（扫描目标表），Time 很大

**根因**：线上业务查询或统计查询长时间持有读锁

**修复**：
1. 等查询结束，或 KILL 可中断的查询
2. 写入时设置更长的等待时间 + 重试：
```python
cur.execute("SET SESSION innodb_lock_wait_timeout = 120")
for attempt in range(3):
    try:
        cur.executemany(sql, params)
        conn.commit()
        break
    except Exception as e:
        conn.rollback()
        if "Lock wait timeout" in str(e) and attempt < 2:
            time.sleep(3)
        else:
            raise
```

### 3. Metadata Lock（DDL 阻塞）

**现象**：`SHOW PROCESSLIST` 中写入语句 State 为 `Waiting for table metadata lock`

**根因**：有 ALTER TABLE / CREATE INDEX 等 DDL 在执行或等待

**修复**：等 DDL 完成，或 KILL DDL 操作

### 4. 连接池泄漏

**现象**：大量 Sleep 连接来自同一 Host，部分持有未提交事务

**根因**：应用连接池未配置 `ConnMaxLifetime` / `ConnMaxIdleTime`

**修复**：
```go
// Go database/sql
db.SetConnMaxLifetime(5 * time.Minute)
db.SetConnMaxIdleTime(3 * time.Minute)
```

## 预防措施清单

- [ ] 所有 `get_connection` 的 finally 中先 rollback 再 close
- [ ] 批量写入设置 `SET SESSION innodb_lock_wait_timeout = 120`
- [ ] 批量写入加重试逻辑（最多 3 次，间隔 3s）
- [ ] 每批 commit 一次，不要在一个大事务里写所有数据
- [ ] 连接池配置 `ConnMaxLifetime` 和 `ConnMaxIdleTime`

## 一键诊断

技能目录下提供了 `diagnose.py` 脚本，可一次性输出所有诊断信息：

```bash
# 使用项目的 shared.db
uv run python /Users/zhenninglang/.factory/skills/mysql-lock-diagnosis/diagnose.py --env .env.prod

# 或指定目标表过滤
uv run python /Users/zhenninglang/.factory/skills/mysql-lock-diagnosis/diagnose.py --env .env.prod --table forge_creator_audience
```
