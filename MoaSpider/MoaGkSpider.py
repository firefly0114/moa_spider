import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from base import SpiderBase

from .MoaIssueSpider import MoaIssueSpider
from .MoaUnitSpider import MoaUnitSpider
from .MoaGkPageSpider import MoaGkPageSpider

class MoaGKSpider(SpiderBase):
    URL="http://www.moa.gov.cn/gk/"


    def request(self):
        resp=self.client.get("http://www.moa.gov.cn/gk/")
        resp.encoding="utf8"
        return resp.text

    def parser(self,html):
        doc=BeautifulSoup(html,features="html.parser")
        unit_list=doc.find_all(class_="gknr_unit")
        print(len(unit_list))
        for unit in unit_list:
            title_elm=unit.find(class_="unit_title")
            a=title_elm.p.a
            category=a.string
            page_url=urljoin(self.URL,a['href'])

            # 通知公告
            # 政策法规
            if category in ("通知公告","政策法规"):
                spider=MoaUnitSpider([category],page_url)

            # 农业农村部公报
            if category in ("农业农村部公报"):
                spider=MoaIssueSpider([category],page_url)

            # 政策解读
            # 财务公开
            # 人事信息
            # 建议提案
            # 规划计划
            # 农事指导
            if category in (
                "政策解读","财务公开","人事信息",
                "建议提案","规划计划","农事指导",
                "政府网站年度报告",
            ):
                spider=MoaGkPageSpider([category],page_url)

            # 政府网站年度报告，不爬
            if category in ("政府网站年度报告"):
                logging.info("跳过 政府网站年度报告")
                continue

            logging.info("开始爬取: {}".format(category))
            spider.run()
            logging.info("爬取完毕: {}".format(category))




        

    def storage(self):
        pass


    def run(self):
        logging.info("爬虫启动")
        data=self.request()
        data=self.parser(data)
        logging.info("爬取退出")
