# DingDing Rss Robot
钉钉 rss 订阅机器人

# 功能

- rss 订阅
- rss 定时推送

# 使用说明

fork 本项目后，需要进行配置后才能正常使用

## rss 源配置

使用数据库管理源打开 rss.db 文件,修改 rss.db 表中的 Rss 表

## 定时配置

修改 `.github/workflows/rssbot.yml` 文件第 8 行 cronb 的表达式

## 配置环境变量

钉钉机器人需要使用 `webhook` 和 `secret` 这两个参考钉钉机器人文档自行申请。

还需要申请一个 `GITHUB_TOKEN`,在 `个人 profile` => `Developer settings` => `Personal access tokens`

然后在项目的 settings 中依次添加 `webhook`,`secret`,`github_token` 三个参数

## ⚠️ 分支问题

默认使用的是 dev 分支，fork 正常只会 fork 主分支，可以参考 https://github.com/LeetaoGoooo/dingding-rssbot/issues/7 进行修改
