# DingDing Rss Robot
钉钉 rss 订阅机器人

# 功能

- rss 订阅
- rss 定时推送

# 使用说明

fork 本项目后，需要进行配置后才能正常使用

## rss 源配置

使用数据库管理源打开 rss.db 文件,修改 rss.db 表中的 Rss 表

```python
class Rss(BaseModel):
    feed = CharField(unique=True)  # 订阅地址
    cover = CharField(max_length=255, null=True)  # 封面(图片地址)
    title = CharField(max_length=20)  # 订阅名称
    url = CharField(max_length=255)   # 网站地址
```


## 定时配置

修改 `.github/workflows/rssbot.yml` 文件第 8 行 cronb 的表达式

⚠️ **频率不要太频繁，避免被误判滥用**

其中 31 和 32 行配置可以设置为自己的邮箱和名称

```yaml
git config --global user.email lineporte@gmail.com
git config --global user.name linep47
```

## 配置环境变量

钉钉机器人需要使用 `WEBHOOK` 和 `SECRET`（对应**加签**） 这两个参考钉钉机器人文档自行申请。

还需要申请一个 `TOKEN`, 点击 [Personal access tokens (classic)](https://github.com/settings/tokens) 申请

然后在项目的 Settings 中依次添加 `WEBHOOK`,`SECRET`,`TOKEN` 三个参数


<img width="1289" alt="image" src="https://user-images.githubusercontent.com/10162120/216604817-28bcdf87-5eff-4362-9c95-968de1913bde.png">


# 效果

<img width="1289" alt="image" src="./screens/效果图.png">
