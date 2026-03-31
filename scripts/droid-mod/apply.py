#!/usr/bin/env python3
"""droid-mod 入口: 备份 → 移除签名 → 应用 mod → 补偿 → 签名

用法:
    python3 apply.py              # 应用全部未修改的 mod
    python3 apply.py 1,4,8       # 只应用指定 mod
    python3 apply.py status      # 仅显示状态
    python3 apply.py restore     # 恢复备份
"""
import subprocess, sys, platform, shutil
from pathlib import Path

DROID = Path.home() / '.local/bin/droid'
DIR = Path(__file__).parent

MODS = [
    (1,  'mod1_truncate_condition',   '命令截断条件短路'),
    (4,  'mod4_diff_lines',           'diff 行数 20→99'),
    (6,  'mod6_custom_model_cycle',   'Ctrl+N 跳过 Copilot'),
    (7,  'mod7_multiline_history',    '多行历史↓键修复'),
    (8,  'mod8_welcome_modified',     'Welcome 橙色 + Modified'),
    (9,  'mod9_custom_effort_levels', 'effort 追加 max'),
    (10, 'mod10_kitty_timeout',       'kitty 超时 200→999ms'),
]
MOD_IDS = {m[0] for m in MODS}
IS_MAC = platform.system() == 'Darwin'


def get_version():
    r = subprocess.run([str(DROID), '--version'], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else 'unknown'


def backup():
    ver = get_version()
    dest = DROID.parent / f'droid.backup.{ver}'
    if not dest.exists():
        shutil.copy2(DROID, dest)
        print(f'  备份: {dest.name}')
    else:
        print(f'  备份已存在: {dest.name}')


def codesign_remove():
    if IS_MAC:
        subprocess.run(['codesign', '--remove-signature', str(DROID)],
                       capture_output=True)


def codesign_sign():
    if IS_MAC:
        subprocess.run(['codesign', '--remove-signature', str(DROID)],
                       capture_output=True)
        subprocess.run(['codesign', '-s', '-', str(DROID)], check=True,
                       capture_output=True)


def run_status():
    subprocess.run([sys.executable, str(DIR / 'status.py')])


def run_restore():
    subprocess.run([sys.executable, str(DIR / 'restore.py')] + sys.argv[2:])


def run_mod(num, name):
    script = DIR / 'mods' / f'{name}.py'
    r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    for line in r.stdout.strip().splitlines():
        print(f'  {line}')
    if r.stderr.strip():
        for line in r.stderr.strip().splitlines():
            print(f'  [err] {line}')
    return r.returncode == 0


def run_compensate(bytes_diff):
    if bytes_diff == 0:
        return True
    r = subprocess.run(
        [sys.executable, str(DIR / 'compensations' / 'comp_universal.py'), str(bytes_diff)],
        capture_output=True, text=True)
    for line in r.stdout.strip().splitlines():
        print(f'  {line}')
    if r.returncode != 0:
        for line in r.stderr.strip().splitlines():
            print(f'  [err] {line}')
        return False
    return True


def main():
    if not DROID.exists():
        print(f'错误: {DROID} 不存在')
        sys.exit(1)

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'status':
            run_status()
            return
        if cmd == 'restore':
            run_restore()
            return

    # 解析 mod 选择
    selected = MOD_IDS
    if len(sys.argv) > 1:
        try:
            selected = {int(x) for x in sys.argv[1].split(',')}
            invalid = selected - MOD_IDS
            if invalid:
                print(f'错误: 未知 mod {invalid}，可选: {sorted(MOD_IDS)}')
                sys.exit(1)
        except ValueError:
            print(f'用法: {sys.argv[0]} [status|restore|1,4,8]')
            sys.exit(1)

    ver = get_version()
    print(f'droid v{ver}\n')

    # 1. 备份
    print('[1/4] 备份')
    backup()

    # 2. 移除签名
    print('[2/4] 移除签名')
    codesign_remove()
    print('  done' if IS_MAC else '  跳过 (非 macOS)')

    # 3. 应用 mod
    print('[3/4] 应用修改')
    size_before = DROID.stat().st_size
    ok, fail = 0, 0
    for num, name, desc in MODS:
        if num not in selected:
            continue
        print(f'  mod{num}: {desc}')
        if run_mod(num, name):
            ok += 1
        else:
            fail += 1
    size_after = DROID.stat().st_size
    byte_diff = size_after - size_before
    print(f'  完成 {ok} 个' + (f', 失败 {fail} 个' if fail else '') +
          (f', 字节变化 {byte_diff:+d}' if byte_diff else ''))

    # 4. 补偿 + 签名
    print('[4/4] 补偿 + 签名')
    comp_ok = True
    if byte_diff > 0:
        comp_ok = run_compensate(byte_diff)
    elif byte_diff == 0:
        print('  无需补偿')
    else:
        print(f'  警告: 字节减少 {byte_diff}，跳过补偿')

    if not comp_ok:
        print(f'\n补偿失败，从备份恢复...')
        run_restore()
        sys.exit(1)

    codesign_sign()
    print('  签名完成' if IS_MAC else '  跳过签名 (非 macOS)')

    print(f'\n完成。新开 droid 窗口验证。')


if __name__ == '__main__':
    main()
