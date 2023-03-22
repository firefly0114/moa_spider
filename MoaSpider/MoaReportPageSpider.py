from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

from base import SpiderBase

from .MoaReportSpider import MoaReportSpider

class MoaReportPageSpider(SpiderBase):
    """爬取翻页内容"""
    def __init__(self,category,page_url):
        super().__init__()
        self.category=category
        self.page_url=page_url
  


    def request(self):
        resp=self.client.get(self.page_url)
        resp.encoding="utf8"
        return resp.text

    def parser(self,html):
        doc=BeautifulSoup(html,features="html.parser")
        # TODO: 解析并爬取文章
        unit_list=doc.find_all(class_="gknr_unit")
        for unit in unit_list:
            content_spider=MoaReportSpider(self.category,content_url)

        # 解析并翻页
        next_page_elm=doc.find("a",string="下一页")
        url=next_page_elm.get("href")
        if not url:
            logging.info("已经爬取到尾页, category:{}".format(self.category))
            return
        next_page_spider=MoaReportPageSpider(self.category,urljoin(self.page_url,url))
        next_page_spider.run()





        

    def storage(self):
        pass


    def run(self):
        data=self.request()
        data=self.parser(data)