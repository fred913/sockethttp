# coding: utf-8

from .request import request, Request, Response


def post(url: str,
         data=None,
         params=None,
         headers=None,
         UserAgent=None,
         timeout=5):
    if data is None:
        data = {}
    if params is None:
        params = {}
    if headers is None:
        headers = {}
    full_url = url[:]
    if not (url.startswith("http://") or url.startswith("https://")):
        if "://" not in url:
            raise ValueError(
                "Unsupported procotol: %s. Did you mean 'http://%s'" %
                (url.split("://")[1]), url)
        raise ValueError("Unsupported procotol: %s" % (url.split("://")[1]))
    url = url.split("://", maxsplit=2)[1]
    host_and_port = url.split("/", maxsplit=2)[0]
    if ":" not in host_and_port:
        host = host_and_port
        port = 80
    else:
        host, port = host_and_port.split(":")
        port = int(port)
    if not len(url.split("/", maxsplit=2)) == 1:
        uri = "/" + url.split("/", maxsplit=2)[1]
    else:
        uri = "/"
    resp = request(host=host,
                   port=port,
                   uri=uri,
                   params=params,
                   method="post",
                   headers=headers,
                   UserAgent=UserAgent,
                   https=full_url.startswith("https://"),
                   timeout=timeout)
    return Response(
        resp, {
            'url': full_url,
            "port": port,
            'host': host,
            'params': params,
            'method': "post",
            'UserAgent': UserAgent or
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0",
            "https": full_url.startswith("https://")
        })
