import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from base import SpiderBase

from .MoaIssueSpider import MoaIssueSpider
from .MoaReportPageSpider import MoaReportPageSpider

class MoaNewsSpider(SpiderBase):
    URL="http://www.moa.gov.cn/xw/"

    def __init__(self):
        super().__init__(self.URL)

    def request(self):
        resp=self.get(self.url)
        resp.encoding="utf8"
        return resp.text

    def parse(self,html):
        doc=BeautifulSoup(html,features="html.parser")
        unit_list=doc.find_all(class_="news-title")
        for unit in unit_list:
            a_elm=unit.find("a")
            category=a_elm.string

            spider=MoaReportPageSpider([category],urljoin(self.URL,a_elm.string))

            logging.info("开始爬取新闻: {}".format(category))
            spider.run()
            logging.info("新闻爬取完毕: {}".format(category))




        

    def storage(self):
        pass


    def run(self):
        logging.info("开始爬取新闻")
        data=self.request()
        data=self.parser(data)
        logging.info("新闻爬取完毕")
