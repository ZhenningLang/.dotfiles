#!/usr/bin/env python3
"""通用字节补偿: 利用所有 mod 产生的死代码区域

用法: python3 comp_universal.py [bytes]
  无参数: 显示当前可用补偿空间
  bytes:  需要补偿的字节数（正数=缩减，负数=扩展）

补偿区域 (按容量排序):
  1. FFH 死代码 (mod1 短路后的不可达区域)    ~100-151B
  2. mod6 validateModelAccess 注释 (3处)      ~36B

原理:
  - ffh_dead: mod1 短路后的不可达代码，最小替换为 ';' (1 byte)
  - comment: /* spaces */ → 调整空格数，最小 /**/ (4 bytes)
"""
import sys, re
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from common import load_droid, save_droid, V

# FFH 死代码最小替换: mod1 已短路返回, 死代码不执行, ';' 即可
FFH_MINIMAL = b';'  # 1 byte


def find_regions(data):
    """扫描所有可用补偿区域，返回 [(name, offset, old_bytes, min_size, type)]"""
    regions = []
    seen = set()

    def add(name, offset, content, min_size, rtype):
        if offset not in seen:
            seen.add(offset)
            regions.append((name, offset, content, min_size, rtype))

    # 1. 截断函数死代码 (mod1 短路后的不可达区域)
    # 定位 mod1 的 early return, 死代码在其后直到第二个 return
    trunc_pat = re.search(
        rb'if\(!0\|\|!' + V + rb'\)return\{text:' + V + rb',isTruncated:!1\}', data)
    if trunc_pat:
        region = data[trunc_pat.start():trunc_pat.start() + 500]
        s1 = region.find(b'isTruncated:!1}')
        if s1 >= 0:
            dead_start = trunc_pat.start() + s1 + 15
            # 结尾: 原版第二个 return 的 isTruncated:!0}
            s2 = region.find(b'isTruncated:!0}', s1 + 15)
            if s2 >= 0:
                dead_end = trunc_pat.start() + s2 + 15
            else:
                # 已补偿: 找 }var 或 }function 作为函数结束标志
                after_dead = data[dead_start:dead_start + 300]
                end_m = re.search(rb'\}var ', after_dead)
                if end_m:
                    dead_end = dead_start + end_m.start()
                else:
                    dead_end = None

            if dead_end and dead_end > dead_start + 1:
                dead_content = data[dead_start:dead_end]
                add('截断函数死代码', dead_start, dead_content, len(FFH_MINIMAL), 'ffh_dead')

    # 2. mod6 注释 (3个函数) — 排除截断函数区域内的注释
    ffh_start = trunc_pat.start() if trunc_pat else -1
    ffh_end = ffh_start + 500 if ffh_start >= 0 else -1
    for m3 in re.finditer(rb'/\*( +)\*/', data):
        if ffh_start >= 0 and ffh_start <= m3.start() <= ffh_end:
            continue
        s = len(m3.group(1))
        if 8 <= s <= 40:
            add('mod6注释', m3.start(), m3.group(0), 4, 'comment')

    return regions


def resize_region(old_bytes, target_size, rtype):
    """生成指定大小的替换内容"""
    if rtype == 'ffh_dead':
        if target_size < len(FFH_MINIMAL):
            return None
        if target_size == 1:
            return b';'
        # ; + spaces 填充
        return b';' + b' ' * (target_size - 1)

    elif rtype == 'comment':
        inner = target_size - 4
        if inner < 0:
            return None
        return b'/*' + b' ' * inner + b'*/'

    return None


def compensate(data, needed_bytes):
    """
    补偿指定字节数。
    needed_bytes > 0: 需要缩减
    needed_bytes < 0: 需要扩展
    返回 (new_data, actual_change)
    """
    regions = find_regions(data)
    if not regions:
        return data, 0

    remaining = needed_bytes
    changes = []

    sorted_regions = sorted(regions, key=lambda r: len(r[2]) - r[3], reverse=True)

    for name, offset, old_bytes, min_size, rtype in sorted_regions:
        if remaining == 0:
            break

        current_size = len(old_bytes)
        avail = current_size - min_size

        if remaining > 0:
            shrink = min(remaining, avail)
            if shrink <= 0:
                continue
            target = current_size - shrink
        else:
            target = current_size + abs(remaining)

        new_bytes = resize_region(old_bytes, target, rtype)
        if new_bytes is None:
            continue

        actual = len(new_bytes) - current_size
        changes.append((name, offset, old_bytes, new_bytes, actual))
        remaining -= (-actual)

    # 从后往前替换
    changes.sort(key=lambda c: c[1], reverse=True)
    total_change = 0
    for name, offset, old_bytes, new_bytes, actual in changes:
        data = data[:offset] + new_bytes + data[offset + len(old_bytes):]
        total_change += actual
        print(f"  {name}: {len(old_bytes)}B → {len(new_bytes)}B ({actual:+d})")

    return data, total_change


def main():
    if len(sys.argv) < 2:
        data = load_droid()
        regions = find_regions(data)
        total = sum(len(r[2]) - r[3] for r in regions)
        print(f"可用补偿区域: {len(regions)} 个, 总容量: {total} bytes\n")
        for name, offset, old_bytes, min_size, rtype in regions:
            avail = len(old_bytes) - min_size
            print(f"  {name:20s}  当前={len(old_bytes):3d}B  可用={avail:3d}B  [{rtype}]")
        return

    try:
        needed = int(sys.argv[1])
    except ValueError:
        print(f"错误: 无效的字节数 '{sys.argv[1]}'")
        sys.exit(1)

    if needed == 0:
        print("无需补偿")
        return

    data = load_droid()
    original_size = len(data)

    regions = find_regions(data)
    total_avail = sum(len(r[2]) - r[3] for r in regions)

    if needed > total_avail:
        print(f"错误: 需要 {needed} bytes 但只有 {total_avail} bytes 可用")
        sys.exit(1)

    print(f"补偿 {needed:+d} bytes:")
    data, actual = compensate(data, needed)
    print(f"实际变化: {actual:+d} bytes")

    if abs(actual) != abs(needed):
        print(f"警告: 未完全补偿 (差 {abs(needed) - abs(actual)} bytes)")
        sys.exit(1)

    assert len(data) == original_size + actual
    save_droid(data)
    print("补偿完成")


if __name__ == '__main__':
    main()
