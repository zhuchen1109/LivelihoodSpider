#coding=utf-8

import hashlib
import urllib
import urlparse
import logging
import tldextract
from scrapy_redis.dupefilter import RFPDupeFilter
from scrapy.utils.request import _fingerprint_cache
from scrapy.utils.python import to_bytes
from w3lib.url import canonicalize_url
from spiders.hfSpider import Hf12345Spider
from constants import *

class HfRFPDupeFilter(RFPDupeFilter):
    """Request Fingerprint duplicates filter"""

    def request_fingerprint(self, request):
        cache = _fingerprint_cache.setdefault(request, None)
        body = request.body
        if cache is None:
            try:
                '''
                    hf12345请求body里以下几个参数是动态的值，这样使请求的签名一直变化，
                    使去重规则无法命中，所以需要自定义规则生成请求的签名
                '''
                hfdomains = Hf12345Spider.allowed_domains
                host = '.'.join(tldextract.extract(request.url)[1:])
                if host in hfdomains:
                    items = dict([(k,v[0]) for k,v in urlparse.parse_qs(body).items()])
                    items.pop(KEY_REQUEST_HF_SYS_RANDOM)
                    items.pop(KEY_REQUEST_HF_TAG)
                    items.pop(KEY_REQUEST_HF_ISSEARCHPASSWORD)
                    body = urllib.urlencode(items)
            except Exception as e:
                logging.error('生成去重签名出错'+e)
                pass

            fp = hashlib.sha1()
            fp.update(to_bytes(request.method))
            fp.update(to_bytes(canonicalize_url(request.url)))
            fp.update(body or b'')
            _fingerprint_cache[request] = fp.hexdigest()
        return _fingerprint_cache[request]