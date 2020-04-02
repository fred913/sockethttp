# coding: utf-8

from sockethttp import get

print(get("http://baidu.com?a=b&c=d").request._data)
