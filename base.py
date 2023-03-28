import requests
import exception
import functools

import logging



class SpiderBase():
    def __init__(self,url,client: requests.Session = None):
        self.url=url
        self.client=client or requests.Session()
        self.client.headers["User-Agent"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

    def run(self):
        try:
            raw_data=self.request()
            parsed_data=self.parse(raw_data)
            self.storage(parsed_data)
        except NotImplementedError:
            pass
        except exception.SpiderCreateError as e:
            logging.error("创建任务失败, 类型:{}, 地址:{}".format(self.__class__.__name__,self.url),
                          exc_info=True)
        except exception.SpiderRequestError as e:
            logging.error("请求失败, 类型:{}, 地址:{}".format(self.__class__.__name__,self.url),
                          exc_info=True)
        except exception.SpiderParseError as e:
            logging.error("解析失败, 类型:{}, 地址:{}".format(self.__class__.__name__,self.url),
                          exc_info=True)
        except exception.SpiderStorageError as e:
            logging.error("存储失败, 类型:{}, 地址:{}".format(self.__class__.__name__,self.url),
                          exc_info=True)
        except exception.SpiderTaskEndError as e:
            logging.info("子任务创建结束, 类型:{}, 地址:{}".format(self.__class__.__name__,self.url))
            raise
        
        logging.info("爬取完成, 类型:{}, 地址:{}".format(self.__class__.__name__,self.url))


    def request(self):
        raise NotImplementedError
    
    def parse(self):
        raise NotImplementedError

    def storage(self):
        raise NotImplementedError

    @functools.wraps(requests.Session.request)
    def do_request(self,*args,**kwargs):
        resp=self.client.request(*args,**kwargs)
        try:
            resp.raise_for_status()
        except requests.RequestException as e:
            raise exception.SpiderRequestError(e)
        return resp
    

    @functools.wraps(requests.Session.get)
    def get(self,*args,**kwargs):
        return self.do_request('get',*args,**kwargs)

    @functools.wraps(requests.Session.get)
    def put(self,*args,**kwargs):
        return self.do_request('put',*args,**kwargs)
    
    @functools.wraps(requests.Session.get)
    def post(self,*args,**kwargs):
        return self.do_request('post',*args,**kwargs)
    
    @functools.wraps(requests.Session.get)
    def delete(self,*args,**kwargs):
        return self.do_request('delete',*args,**kwargs)
    
    @functools.wraps(requests.Session.get)
    def head(self,*args,**kwargs):
        return self.do_request('head',*args,**kwargs)
    
    @functools.wraps(requests.Session.get)
    def options(self,*args,**kwargs):
        return self.do_request('options',*args,**kwargs)



    

