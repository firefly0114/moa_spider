from bs4 import BeautifulSoup
from urllib.parse import urljoin

from base import SpiderBase

class MoaSpider(SpiderBase):
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
            # 通知公告
            # 农业农村部公报
            # 政策法规
            # 政策解读
            # 财务公开
            # 人事信息
            # 建议提案
            # 规划计划
            # 农事指导
            # 政府网站年度报告
            a=title_elm.p.a
            title=a.string
            href=a['href']
            print(title,urljoin(self.URL,href))


        

    def storage(self):
        pass


    def run(self):
        data=self.request()
        data=self.parser(data)