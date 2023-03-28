from MoaSpider import MoaGkSpider
from MoaSpider import MoaNewsSpider

def main():
    gk_spider=MoaGkSpider()
    gk_spider.run()
    news_spider=MoaNewsSpider()
    news_spider.run()

if __name__ == "__main__":
    main()