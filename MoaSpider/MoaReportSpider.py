from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import requests

from base import SpiderBase

class MoaReportSpider(SpiderBase):
    """爬取指定的新闻或公报（农业农村部）"""

    def __init__(self,category,url):
        super().__init__(url)
        self.category=category


    def request(self):
        resp=self.get(self.url)
        resp.encoding="utf8"
        return resp.text

    def parse(self,html):
        doc=BeautifulSoup(html,features="html.parser")
        article=doc.find(class_="main bjjM hd_wzxq")
        title=article.find(class_="bjjMTitle").string
        author_box=article.find(class_="bjjMAuthorBox")
        pubtime=author_box.children[0].span.string
        auther=author_box.children[1].span.string
        source=author_box.children[2].span.string
        text=article.find(class_="TRS_Editor").string

        result={
            "category":self.category,
            "title":title,
            "pubtime":pubtime,
            "auther":auther,
            "source":source,
            "text":text,
        }
        return result
