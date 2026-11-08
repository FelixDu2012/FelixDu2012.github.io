#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
 Felix Du 个人博客 · 发布程序（朋友圈式发布流程）
============================================================
 功能：
  1. 每天无需修改源码即可添加博客内容（文字 / 图片 / 视频 / 音频）
  2. 支持表情、特殊符号，并可为每篇内容选择字体
  3. 多媒体文件单独存放到 media/ 目录（不做 Base64，加载快）
  4. 内容写入 posts.json（网页按时间倒序展示）
  5. 自动 push 到 GitHub，实时显示推送进度与成功/失败状态
  6. 本地同时保留一份内容副本（本地仓库 + _backup 备份）

 用法：  python publish.py
============================================================
"""

import os
import sys
import json
import shutil
import subprocess
import datetime
import hashlib
import time
import re

# ---------------- 路径与常量 ----------------
REPO_DIR   = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(REPO_DIR, "posts.json")
MEDIA_DIR  = os.path.join(REPO_DIR, "media")
BACKUP_DIR = os.path.join(REPO_DIR, "_backup")

# 字体选项（样式已硬编码进 index.html，这里只存关键字）
FONTS = [
    ("sans",  "默认黑体（思源黑体）"),
    ("serif", "衬线体（Liberation Serif）"),
    ("mono",  "等宽字体（Consolas）"),
    ("kai",   "楷体（楷体 / Kaiti）"),
    ("cute",  "可爱风（加粗圆润）"),
]

# 表情与特殊符号（可直接输入，也可从这里挑选）
EMOJIS = ("😀 😄 😁 😂 🤣 😊 😍 🥰 😘 😎 🤔 😅 😭 😢 😡 😱 🤯 "
          "👍 👎 👏 🙏 💪 🎉 🎂 🎁 🎈 🎮 🎵 🎶 ❤️ 💛 💚 💙 💜 🧡 "
          "⭐ 🌟 🔥 ✨ 🌈 ☀️ 🌙 ☁️ ❄️ 🌸 🌺 🍀 🌻 🐱 🐶 🐼 🐰 🦊 "
          "🍕 🍔 🍟 🍦 🍰 🍎 🍉 🥤 ⚽ 🏀 🎾 🚀 🎯 🎲")
SPECIAL = "★ ☆ ♥ ♡ ♪ ♫ ☀ ☁ ☂ ☃ ✿ ❀ ✈ ☮ ✌ ❤ → ← ↑ ↓ ☞ ☜ "
IMAGE_EXT  = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
VIDEO_EXT  = {".mp4", ".webm", ".mov", ".m4v", ".avi"}
AUDIO_EXT  = {".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac"}


# ---------------- 工具函数 ----------------
def setup_console():
    """尽量把 Windows 控制台设为 UTF-8，保证表情/中文正常显示。"""
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            ctypes.windll.kernel32.SetConsoleCP(65001)
        except Exception:
            pass


def clear():
    os.system("cls" if sys.platform == "win32" else "clear")


def banner():
    print("=" * 58)
    print("   Felix Du 的博客 · 发布程序  (朋友圈式发布)")
    print("=" * 58)
    now = datetime.datetime.now()
    print("   今天：%s  %s" % (now.strftime("%Y年%m月%d日"), "星期" + "一二三四五六日"[now.weekday()]))
    print("   主题色：%s" % theme_color(now))
    print("=" * 58)


def theme_color(dt=None):
    """按日期生成主题色（与网页算法一致）。"""
    dt = dt or datetime.date.today()
    s = "%d-%02d-%02d" % (dt.year, dt.month, dt.day)
    h = 0
    for ch in s:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    hue = h % 360
    return "hsl(%d, 72%%, 62%%)" % hue


def read_text(prompt):
    """读取一行输入，兼容中文/表情。"""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    line = sys.stdin.readline()
    if not line:
        return ""
    return line.rstrip("\n").rstrip("\r")


def read_multiline(prompt):
    """读取多行文本，输入空行结束。"""
    print(prompt)
    print("（每行一条，输入空行结束；可直接粘贴表情/符号）")
    lines = []
    while True:
        line = read_text("  > ")
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


def pick_choice(options, prompt="请选择"):
    """通用数字选择。options: [(value, label), ...]"""
    print()
    for i, (_, label) in enumerate(options, 1):
        print("  %d. %s" % (i, label))
    while True:
        s = read_text(prompt + " (1-%d，回车=1)： " % len(options)).strip()
        if s == "":
            return options[0][0]
        if s.isdigit() and 1 <= int(s) <= len(options):
            return options[int(s) - 1][0]
        print("  ⚠ 输入无效，请重新选择。")


def choose_font():
    print("\n—— 选择这篇内容的字体 ——")
    return pick_choice(FONTS, "选择字体")


def choose_media(kind):
    """让用户选择媒体文件（支持拖入路径 / 输入路径）。返回文件路径列表。"""
    exts = IMAGE_EXT if kind == "image" else (VIDEO_EXT if kind == "video" else AUDIO_EXT)
    label = {"image": "图片", "video": "视频", "audio": "音频"}[kind]
    print("\n—— 添加%s ——" % label)
    print("（直接把文件拖进窗口即可得到路径，回车跳过）")
    paths = []
    max_n = 1 if kind != "image" else 9  # 视频/音频一篇一个，图片最多 9 张
    while len(paths) < max_n:
        p = read_text("  文件路径（回车跳过）： ").strip().strip('"').strip("'")
        if p == "":
            break
        if not os.path.isfile(p):
            print("  ⚠ 文件不存在：%s" % p)
            continue
        ext = os.path.splitext(p)[1].lower()
        if ext not in exts:
            print("  ⚠ 不支持的格式（%s），%s支持：%s" % (ext, label, " ".join(sorted(exts))))
            continue
        paths.append(p)
        if kind != "image":
            break
    return paths


def emoji_helper():
    print("\n—— 表情 & 特殊符号 ——")
    print("  表情：" + EMOJIS)
    print("  符号：" + SPECIAL)
    print("  （小技巧：Windows 按 Win+. 可打开系统表情面板直接输入）")


def save_posts(post):
    """把新内容追加到 posts.json（保留原有内容，倒序交给网页处理）。"""
    data = {"posts": []}
    if os.path.exists(POSTS_FILE):
        try:
            with open(POSTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"posts": []}
    if not isinstance(data.get("posts"), list):
        data["posts"] = []
    data["posts"].append(post)
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    backup()


def backup():
    """本地保留一份内容副本（posts.json 与 media 目录）。"""
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        shutil.copy2(POSTS_FILE, os.path.join(BACKUP_DIR, "posts.json"))
        media_backup = os.path.join(BACKUP_DIR, "media")
        if os.path.isdir(MEDIA_DIR):
            if os.path.isdir(media_backup):
                shutil.rmtree(media_backup)
            shutil.copytree(MEDIA_DIR, media_backup)
    except Exception as e:
        print("  ⚠ 本地备份失败（不影响发布）：%s" % e)


def copy_media(src, kind, now):
    """把媒体复制到 media/ 目录，返回相对路径。"""
    os.makedirs(MEDIA_DIR, exist_ok=True)
    ext = os.path.splitext(src)[1].lower()
    digest = hashlib.md5((src + str(now.timestamp())).encode()).hexdigest()[:8]
    name = "%s-%s-%s%s" % (now.strftime("%Y%m%d"), now.strftime("%H%M%S"), digest, ext)
    dst = os.path.join(MEDIA_DIR, name)
    shutil.copy2(src, dst)
    return "media/" + name


def new_id(now):
    return "%s-%s-%s" % (now.strftime("%Y%m%d"), now.strftime("%H%M%S"),
                         hashlib.md5(str(now.timestamp()).encode()).hexdigest()[:6])


# ---------------- Git 推送 ----------------
def run_git(args, show_output=True):
    """运行 git 命令，返回 (returncode, output)。"""
    try:
        proc = subprocess.run(
            ["git"] + args,
            cwd=REPO_DIR, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except FileNotFoundError:
        return 127, "未找到 git，请确认已安装 Git。"


def git_push_with_progress():
    """自动 push 到 GitHub，实时显示进度与成功/失败状态。"""
    print("\n—— 正在推送到 GitHub ——")

    # 1) 检查 git 仓库
    rc, out = run_git(["rev-parse", "--is-inside-work-tree"], show_output=False)
    if rc != 0:
        print("  ✗ 当前目录不是 git 仓库，无法推送。")
        return False

    # 2) 检查远程
    rc, remote = run_git(["remote", "get-url", "origin"], show_output=False)
    if rc != 0 or not remote.strip():
        print("  ✗ 未配置远程仓库 origin。")
        print("    请先执行： git remote add origin <你的仓库地址>")
        return False
    print("  远程仓库：%s" % remote.strip())

    # 3) git add
    rc, out = run_git(["add", "-A"])
    if rc != 0:
        print("  ✗ git add 失败：%s" % out)
        return False

    # 4) git commit（无改动则跳过）
    rc, out = run_git(["commit", "-m", "发布新内容 " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")])
    if rc != 0:
        if "nothing to commit" in out or "无文件要提交" in out:
            print("  · 没有新的改动，跳过提交。")
        else:
            print("  ✗ git commit 失败：%s" % out)
            return False

    # 5) git push（实时进度）
    print("  推送中……")
    sys.stdout.flush()
    try:
        proc = subprocess.Popen(
            ["git", "push", "--progress", "origin", "HEAD"],
            cwd=REPO_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace",
        )
        out_lines = []
        for line in proc.stdout:
            line = line.rstrip()
            if line:
                out_lines.append(line)
                # 只显示进度类信息，避免刷屏
                if any(k in line for k in ("Writing objects", "Counting objects",
                                           "Compressing objects", "Enumerating", "Total", "remote:")):
                    print("  " + line.strip())
        proc.wait()
        code = proc.returncode
        full = "\n".join(out_lines)
    except FileNotFoundError:
        print("  ✗ 未找到 git。")
        return False

    if code == 0:
        print("\n  ✔ 推送成功！网站已更新：https://FelixDu2012.github.io")
        return True
    else:
        print("\n  ✗ 推送失败（git push 返回码 %d）。" % code)
        if full:
            print("  详情：%s" % full[-400:])
        print("  常见原因：网络问题 / 鉴权失败（需在 GitHub 生成 Personal Access Token 并配置）。")
        return False


# ---------------- 主流程 ----------------
def main():
    setup_console()
    clear()
    banner()

    print("\n开始发布新内容……\n")

    # 1) 文字内容
    emoji_helper()
    print()
    content = read_multiline("—— 输入文字内容 ——")
    if content.strip() == "":
        # 允许纯媒体内容
        ok = read_text("  内容为空，仅发布媒体？(y/n，默认 n)： ").strip().lower()
        if ok not in ("y", "yes"):
            print("  已取消发布。")
            return

    # 2) 字体
    font = choose_font()

    # 3) 媒体
    images = choose_media("image")
    video = choose_media("video")
    audio = choose_media("audio")

    # 4) 汇总确认
    now = datetime.datetime.now()
    media_list = []
    copied = []
    for img in images:
        copied.append((img, "image"))
    for v in video:
        copied.append((v, "video"))
    for a in audio:
        copied.append((a, "audio"))

    print("\n" + "=" * 58)
    print("  发布预览")
    print("=" * 58)
    print("  日期：%s %s" % (now.strftime("%Y-%m-%d"), now.strftime("%H:%M")))
    print("  字体：%s" % dict(FONTS).get(font, font))
    print("  内容：%s" % (content[:60] + ("…" if len(content) > 60 else "") or "(无)"))
    if images:
        print("  图片：%d 张" % len(images))
    if video:
        print("  视频：%d 个" % len(video))
    if audio:
        print("  音频：%d 个" % len(audio))
    print("=" * 58)

    confirm = read_text("  确认发布？(y/n，默认 y)： ").strip().lower()
    if confirm in ("n", "no"):
        print("  已取消发布。")
        return

    # 5) 复制媒体文件
    for src, kind in copied:
        rel = copy_media(src, kind, now)
        media_list.append({"type": kind, "src": rel})
        print("  已复制媒体：%s -> %s" % (os.path.basename(src), rel))

    # 6) 写入 posts.json
    post = {
        "id": new_id(now),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "font": font,
        "content": content,
        "media": media_list,
    }
    save_posts(post)
    print("  已写入 posts.json（本地副本：%s）" % BACKUP_DIR)

    # 7) 推送
    success = git_push_with_progress()

    print("\n" + "=" * 58)
    if success:
        print("  ✔ 发布完成！")
    else:
        print("  ⚠ 内容已保存在本地，但推送未成功。")
        print("    你可以稍后手动执行： git push origin HEAD")
    print("  本地内容已保留（仓库目录 + %s）。" % BACKUP_DIR)
    print("=" * 58)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  已退出。")
    except Exception as e:
        print("\n  ✗ 发生错误：%s" % e)
