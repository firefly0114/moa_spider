from bs4 import BeautifulSoup
from urllib.parse import urljoin

from base import SpiderBase


class MoaGkDocumentSpider(SpiderBase):
    """爬取指定的文章"""

    def __init__(self,category,page_url):
        super().__init__()
        self.category=category
        self.page_url=page_url


    def request(self):
        resp=self.client.get(self.page_url)
        resp.encoding="utf8"
        resp.raise_for_status()
        return resp.text

    def parser(self,html):
        doc=BeautifulSoup(html,features="html.parser")
        content_elm=doc.find(class_="gsj_content")
        title=content_elm.find(class_="xxgk_title").string
        subtitle_elm=content_elm.find(class_="subtitle").string
        pubtime=subtitle_elm.find(class_="pubtime").string.lstrip("发布时间：")
        source=subtitle_elm.find(class_="pubtime source").string.lstrip("来源：")
        text=doc.find(class_="gsj_htmlcon_bot").string

        result={
            "category":self.category,
            "title":title,
            "pubtime":pubtime,
            "source":source,
            "text":text,
        }
        return result,None
        

    def storage(self):
        pass


    def run(self):
        data=self.request()
        data=self.parser(data)