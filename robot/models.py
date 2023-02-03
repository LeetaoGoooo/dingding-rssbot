from peewee import *
import datetime

db = SqliteDatabase('rss.db')


class BaseModel(Model):
    class Meta:
        database = db


class Rss(BaseModel):
    feed = CharField(unique=True)  # 订阅地址
    cover = CharField(max_length=255, null=True)  # 封面(图片地址)
    title = CharField(max_length=20)  # 订阅名称
    url = CharField(max_length=255)   # 网站地址


class History(BaseModel):
    url = CharField(max_length=255)
    publish_at = DateField(default=datetime.datetime.now)


def create_tables():
    with db:
        db.create_tables([Rss, History])
