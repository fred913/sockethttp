# coding: utf-8

try:
    from setuptools import setup
except BaseException:
    from distutils import setup
from sockethttp import __version__
import os

name = "sockethttp"
resources = []

for dirpath, dirnames, filenames in os.walk(name):
    for file in filenames:
        if dirpath == name:  # 如果是当前项目目录的话
            if not file.endswith('.py'):  # 不取py文件，因为python文件不是其他资源，是程序
                resources.append(file)
        else:
            basepath = dirpath.split(os.path.sep,
                                     1)[1]  # nn_test/img路径是这样，取img
            resources.append(os.path.join(basepath,
                                          file))  # 拼好的路径就是img/example.jpg

setup(
    name=name,
    version=__version__,
    description='the faster http/1.1 client than requests',
    author='Sheng Fan',
    author_email='1175882937@qq.com',
    url='https://github.com/fred913/sockethttp',
    packages=['sockethttp'],
    long_description="The faster http/1.1 client than requests."
    "Supported methods: GET and POST",
    license="GPL-2.0",
    platforms=["any"],
)
