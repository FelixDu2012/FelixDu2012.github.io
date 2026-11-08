# Felix Du 的个人博客

部署于 GitHub Pages：**https://FelixDu2012.github.io**

这是一个单页个人博客 + 朋友圈式发布系统。日常发布内容时，**无需修改任何源码**，只要运行一个 Python 程序即可。

## 项目结构

```
├── index.html     # 博客主页（字体/签名/皮肤等已 base64 内嵌，单文件）
├── posts.json     # 博客内容数据（文字 + 媒体路径）
├── media/         # 上传的多媒体文件（图片/视频/音频，单独存放，加载快）
├── publish.py     # 朋友圈式发布程序（核心工具）
├── build.py       # 重新构建 index.html 的脚本（一般无需手动运行）
├── _backup/       # 本地内容副本（posts.json + media 的自动备份）
└── README.md
```

## 如何发布新内容

```bash
python publish.py
```

按提示操作即可：

1. **输入文字**（多行，支持表情、特殊符号，可直接粘贴；Windows 下按 `Win + .` 打开表情面板）
2. **选择字体**（黑体 / 衬线 / 等宽 / 楷体 / 可爱风）
3. **添加媒体**（图片最多 9 张、视频 1 个、音频 1 个，把文件拖进窗口即可得到路径）
4. **确认预览** → 自动写入 `posts.json`、复制媒体到 `media/`、**自动 push 到 GitHub**
5. 程序会**实时显示推送进度**，最后显示**成功 / 失败**状态

> 本地会同时保留一份内容副本（仓库目录 + `_backup/`），即使推送失败也不会丢失内容。

## 网页功能

- 固定内容在开头（姓名、签名、座右铭、名字来源、生日、联系方式、教育经历、Minecraft）
- 博客内容**按时间倒序**展示，**向下滚动加载更多**
- **关键词搜索** 与 **按日期筛选**
- **鼠标移动**（背景光晕）、**向下滚动**（内容淡入）、卡片悬停等**动画效果**
- **主题色按当天日期通过算法自动生成**，每天颜色不同
- 支持**中文 / English** 双语切换
- 响应式布局，手机 / 平板 / 电脑自适应

## 首次部署（仅需一次）

```bash
git init
git add -A
git commit -m "init blog"
git remote add origin https://github.com/FelixDu2012/FelixDu2012.github.io.git
git push -u origin main
```

在 GitHub 仓库 **Settings → Pages** 中，将 Source 设为 `main` 分支即可（`<用户名>.github.io` 仓库通常默认已开启）。

## 鉴权说明

`publish.py` 通过本机 Git 凭据推送。若推送提示鉴权失败，请在 GitHub 生成一个 Personal Access Token（勾选 `repo` 权限），并用它作为密码配置：

```bash
git config --global credential.helper manager
# 下次 push 时用户名填 GitHub 账号，密码填 Token
```
