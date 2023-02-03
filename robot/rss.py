# -*- encoding: utf-8 -*-

"""
rss.py

钉钉 Rss 机器人
推送 Rss 信息到钉钉机器人Api
 
"""
from datetime import datetime, timedelta
from itertools import takewhile
import feedparser
from dingtalkchatbot.chatbot import DingtalkChatbot, CardItem
import dateparser
from models import db, Rss, History
import os


class RssRobot:
    def __init__(self):
        # 说明文档的效果图中的 post_cover
        self.post_cover = "https://leetao.zhubai.love/api/wechat/miniprogram_qrcode?page=pages%2Fpublication%2Fpublication&publication_id=2170089804120211456&scene=token%3Dleetao&width=200"
        self.robot = DingtalkChatbot(
            os.environ.get("DD_WEBHOOK"),
            pc_slide=True, secret=os.environ.get("DD_SECRET"))
        self.remove_old_history()

    @property
    def sended_urls(self):
        return [rss_history.url for rss_history in History.select()]

    @property
    def subscriptions(self):
        return Rss.select()

    def get_post_cards(self):
        feeds = []
        for subscription in self.subscriptions:
            feed = feedparser.parse(subscription.feed)
            pic_url = subscription.cover if subscription.cover else self.post_cover
            feed_header = CardItem(
                title=subscription.title, url=subscription.url, pic_url=pic_url)
            posts = self.get_posts(feed.entries)
            if posts:
                feeds.append([feed_header, *posts])
        return feeds

    def get_posts(self, entries):
        post_cards = []
        post_urls = []
        for entry in takewhile(self.is_not_sended, entries):
            post_cards.append(CardItem(title=entry.title,
                              url=entry.link, pic_url=self.post_cover))
            post_urls.append(History(url=entry.link))
        with db.atomic():
            History.bulk_create(post_urls, batch_size=100)
        return post_cards

    def is_not_sended(self, url):
        return url not in self.sended_urls

    def is_today(self, entry):
        return dateparser.parse(entry['updated']).date() == datetime.today().date()

    def send_rss(self):
        post_cards = self.get_post_cards()
        for post_card in post_cards:
            self.robot.send_feed_card(post_card)

    def remove_old_history(self):
        # 只保留最近一周的记录
        week_date_range = datetime.now() + timedelta(days=-7)
        History.delete().where(History.publish_at <
                               week_date_range.strftime("%Y-%m-%d")).execute()


def send_rss():
    rss_bot = RssRobot()
    rss_bot.send_rss()


if __name__ == '__main__':
    send_rss()
