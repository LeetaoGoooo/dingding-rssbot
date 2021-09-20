# -*- encoding: utf-8 -*-

"""
rss.py

钉钉 Rss 机器人
推送 Rss 信息到钉钉机器人Api
 
"""
from datetime import datetime,timedelta
import feedparser
from dingtalkchatbot.chatbot import DingtalkChatbot, CardItem, ActionCard
import dateparser
from models import db, Rss, History
import os

class RssRobot:
    def __init__(self):
        self.robot = DingtalkChatbot(
            os.environ.get("DD_WEBHOOK"),
            pc_slide=True, secret=os.environ.get("DD_SECRET"))

    def parse_rss(self):
        # self.remove_old_history()
        rss_list = Rss.select()
        rss_card_dict = {}
        post_url_list = [rss_history.url for rss_history in
                         History.select().where(History.publish_at == datetime.today().strftime("%Y-%m-%d"))]
        for rss in rss_list:
            rss_history_list = []
            card_list = [
                CardItem(title=rss.title, url=rss.url, pic_url=rss.cover)]
            feed = feedparser.parse(rss.feed)            
            for entry in feed.entries:
                if entry.link not in post_url_list: # and self.is_today(entry):
                    card_list.append(CardItem(title=f'{entry.title}', url=entry.link,
                                            pic_url='https://ftp.bmp.ovh/imgs/2020/07/6cdb9f606677c9e3.jpg'))
                    rss_history_list.append(History(url=entry.link))

            if len(card_list) > 1:
                rss_card_dict[rss.title] = card_list
                with db.atomic():
                    History.bulk_create(rss_history_list, batch_size=10)

        return rss_card_dict

    def is_today(self, entry):
        return dateparser.parse(entry['updated']).date() == datetime.today().date()

    def send_rss(self):
        rss_card_dict = self.parse_rss()
        for key in rss_card_dict:
            self.robot.send_feed_card(rss_card_dict[key])
    
    def remove_old_history(self):
        # 只保留最近一周的记录
        week_date_range = datetime.now() + timedelta(days=-7)
        History.delete().where(History.publish_at < week_date_range.strftime("%Y-%m-%d")).execute()


def send_rss():
    rss_bot = RssRobot()
    rss_bot.send_rss()

if __name__ == '__main__':
    send_rss()
