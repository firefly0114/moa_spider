class SpiderError(Exception):
    pass

class SpiderCreateError(SpiderError):
    pass

class SpiderRequestError(SpiderError):
    pass

class SpiderParseError(SpiderError):
    pass

class SpiderStorageError(SpiderError):
    pass
