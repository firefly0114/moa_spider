from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import requests

from base import SpiderBase

class MoaReportSpider(SpiderBase):
    """爬取指定的新闻或公报（农业农村部）"""

    def __init__(self,category,page_url):
        super().__init__()
        self.category=category
        self.page_url=page_url


    def request(self):
        try:
            resp=self.get(self.page_url)
            resp.encoding="utf8"
        except requests.HTTPError as e:
            return None,e
        return resp.text,None

    def parser(self,html):
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
        return result,None

        

    def storage(self):
        pass


    def run(self):
        data,status=self.request()
        if status:
            logging.error("爬取报道失败, category:{}, title:{}".format(self.category,self.title))
            return

        data,status=self.parser(data)
        if status:
            logging.error("爬取报道失败, category:{}, title:{}".format(self.category,self.title))
            return

        status=self.storage(data)
        if status:
            logging.error("爬取报道失败, category:{}, title:{}".format(self.category,self.title))
            return
        
        logging.error("爬取报道成功, category:{}, title:{}".format(self.category,self.title))
        return
