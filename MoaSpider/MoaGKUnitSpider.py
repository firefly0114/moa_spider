from bs4 import BeautifulSoup
from urllib.parse import urljoin

from base import SpiderBase
from .MoaReportPageSpider import MoaReportPageSpider

class MoaGkUnitSpider(SpiderBase):
    """爬取分子单元块的页面"""
    def __init__(self,category,url):
        super().__init__(url)
        self.category=category


    def request(self):
        resp=self.get(self.url)
        resp.encoding="utf8"
        return resp.text

    def parse(self,html):
        doc=BeautifulSoup(html,features="html.parser")
        unit_list=doc.find_all(class_="gknrtitle")
        print(len(unit_list))
        for unit in unit_list:
            unit_title=unit.span.string
            href=unit.a['href']
            page_url=urljoin(self.url,href)
            MoaReportPageSpider(page_url)
            stop=MoaReportPageSpider.run()
            