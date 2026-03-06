#!/usr/bin/env bun

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import readline from 'node:readline';
import { PassThrough } from 'node:stream';

const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  console.log(`用法: bun option_key_probe.mjs [--log /tmp/file.log]\n\n功能:\n- 记录 stdin 原始字节(data 事件)\n- 记录 Bun/readline 解析后的 keypress 事件\n- 方便对比 Option+Left/Right/Backspace 在当前终端里的真实行为\n\n退出: Ctrl+C\n`);
  process.exit(0);
}

const logIndex = args.indexOf('--log');
const logPath = logIndex >= 0 && args[logIndex + 1]
  ? path.resolve(args[logIndex + 1])
  : path.join(os.tmpdir(), 'droid-option-key-probe.log');

fs.mkdirSync(path.dirname(logPath), { recursive: true });
const logStream = fs.createWriteStream(logPath, { flags: 'w' });

const parserInput = new PassThrough();
const rl = readline.createInterface({ input: parserInput, escapeCodeTimeout: 0 });
readline.emitKeypressEvents(parserInput, rl);

function now() {
  return new Date().toISOString();
}

function toHex(buffer) {
  return [...buffer].map((b) => b.toString(16).padStart(2, '0')).join(' ');
}

function safeJson(value) {
  return JSON.stringify(value).replaceAll('\\u001b', '\\x1b');
}

function logLine(type, payload) {
  const line = `[${now()}] [${type}] ${payload}`;
  console.log(line);
  logStream.write(line + '\n');
}

function cleanup(exitCode = 0) {
  try {
    if (process.stdin.isTTY) {
      process.stdin.setRawMode(false);
    }
  } catch {}
  rl.close();
  parserInput.end();
  logLine('exit', `日志已写入 ${logPath}`);
  logStream.end(() => process.exit(exitCode));
}

logLine('start', `bun=${process.versions.bun} node=${process.versions.node} pid=${process.pid}`);
logLine('start', `logPath=${logPath}`);
logLine('hint', '请依次按 Option+Left / Option+Right / Option+Backspace；按 Ctrl+C 退出');

parserInput.on('keypress', (str, key) => {
  logLine('keypress', safeJson({ str, key }));
});

process.stdin.on('data', (chunk) => {
  const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
  logLine('raw', safeJson({ utf8: buffer.toString('utf8'), hex: toHex(buffer), length: buffer.length }));
  parserInput.write(buffer);
});

process.stdin.on('error', (error) => {
  logLine('stdin-error', safeJson({ message: error.message }));
  cleanup(1);
});

process.on('SIGINT', () => cleanup(0));
process.on('SIGTERM', () => cleanup(0));

if (process.stdin.isTTY) {
  process.stdin.setRawMode(true);
}
process.stdin.resume();
