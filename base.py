import requests
import exception
import functools

class SpiderBase():
    def __init__(self):
        self.client=requests.Session()
        self.client.headers["User-Agent"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

    @functools.wraps(requests.Session.request)
    def do_request(self,*args,**kwargs):
        resp=self.client.request(*args,**kwargs)
        try:
            resp.raise_for_status()
        except requests.RequestException as e:
            raise exception.SpiderRequestError(e)
        return resp
    

    get=functools.wraps(requests.Session.get)(functools.partial(do_request,method='get'))
    # def get(self,*args,**kwargs):
    #     return self.do_request('get',*args,**kwargs)

    put=functools.wraps(requests.Session.put,functools.partial(do_request,'put'))
    post=functools.wraps(requests.Session.post,functools.partial(do_request,'post'))
    delete=functools.wraps(requests.Session.delete,functools.partial(do_request,'delete'))
    head=functools.wraps(requests.Session.head,functools.partial(do_request,'head'))
    options=functools.wraps(requests.Session.options,functools.partial(do_request,'options'))


    

