from bs4 import BeautifulSoup
from urllib.parse import urljoin

from base import SpiderBase


class MoaGkDocumentSpider(SpiderBase):
    """爬取指定的文章"""

    def request(self):
        resp=self.get(self.url)
        resp.encoding="utf8"
        return resp.text

    def parse(self,html):
        doc=BeautifulSoup(html,features="html.parser")
        content_elm=doc.find(class_="gsj_content")
        title=content_elm.find(class_="xxgk_title").string
        subtitle_elm=content_elm.find(class_="subtitle")
        pubtime=subtitle_elm.find(class_="pubtime").string.lstrip("发布时间：")

        result={
            "category":self.category,
            "title":title,
            "pubtime":pubtime,
        }

        source_elm=subtitle_elm.find(class_="pubtime source")
        if source_elm:
            result["source"]=source_elm.string.lstrip("来源：")

        result["text"]=doc.find(class_="gsj_htmlcon_bot").string


        return result
        