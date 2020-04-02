#!/usr/bin/python3
# coding: utf-8

import socket
import sys
import re
from urllib import parse
import zlib
import json

newline = "\n"


def isIP(str):
    p = re.compile(
        r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False


class _callable_str(str):
    def __init__(self, data):
        super(self, str).__init__(data)

    def __call__(self):
        return self.__str__()


class Request:
    def __init__(self, data: dict):
        self._data = data

    def __getattr__(self, key):
        return self._data[key]


class Response:
    def __init__(self, response_data, request_data):
        self._response_data = response_data
        self.coding = "utf-8"
        self._request_data = request_data

    @classmethod
    def parse_header(self, header_data, coding=None):
        if coding is None:
            coding = self.coding
        if not isinstance(header_data, str):
            if isinstance(header_data, bytes):
                header_data = header_data.decode(coding)

    @property
    def _body_data(self):
        result = {}
        resp = self._response_data.split(b"\n")[1:]
        body = b""
        sep = b"\r\n\r\n"
        body = self._response_data.split(sep, maxsplit=2)[1]
        return body

    @property
    def text(self):
        return self._body_data.decode(self.coding)

    @property
    def content(self):
        return self._body_data

    @property
    def encode(self):
        return self.coding

    @encode.setter
    def set_encode(self, val):
        self.coding = val

    @property
    def json(self):
        return json.loads(self.text, encoding=self.coding)

    @property
    def headers(self):
        result = {}
        resp = self._response_data.split("\n")[1:]
        head_str = []
        for i in resp:
            if i.strip():
                head_str.append(i.decode(self.coding))
            else:
                break
        head = {}
        for i in head_str:
            head[i.split(':')[0].strip()] = i.split(':', maxsplit=2)[1].strip()
        return head

    @property
    def request(self):
        return Request(self._request_data)


def recvall(the_socket, timeout=5):
    total_data = b""
    the_socket.settimeout(timeout // 2)
    data = the_socket.recv(1024)
    total_data += data
    num = len(data)
    while len(data) > 0:
        data = the_socket.recv(1024)
        num += len(data)
        total_data += data
    return total_data


def request(host,
            port=80,
            uri="/",
            params={},
            method="GET",
            headers={},
            body=None,
            UserAgent=None,
            timeout=5,
            https=False):
    if https:
        raise ValueError("Unsupported procotol: https")
    if params is not {}:
        if "?" not in uri:
            uri += "?"
        elif uri.endswith("?"):
            uri += parse.urlencode(params)
        else:
            uri += "&" + parse.urlencode(params)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = f"""{method.strip().upper()} {uri} HTTP/1.1
Host: {host}{"" if port in [443, 80] else (":" + str(port))}
User-Agent: {UserAgent if UserAgent else "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"}
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Pragma: no-cache
Cache-Control: no-cache
{newline.join(["%s: %s" % (k, headers[k]) for k in headers])}
{body}
""".encode()
    s.connect((socket.gethostbyname(host) if not isIP(host) else host, port))
    s.sendall(data)
    try:
        data = recvall(s, timeout=timeout)
    except socket.timeout:
        raise TimeoutError("Time out on receiving data")
    s.close()
    return data


if __name__ == "__main__":
    print(get("http://www.baidu.com").text)
