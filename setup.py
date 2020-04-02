# coding: utf-8

try:
    from setuptools import setup
except BaseException:
    from distutils import setup
from sockethttp import __version__
import os
import platform

if str(platform.python_version()).startswith("2.7"):
    print(
        "Warning: sockethttp has not been tested on this Python version, which may cause bugs"
    )

name = "sockethttp"
resources = []

for dirpath, dirnames, filenames in os.walk(name):
    for file in filenames:
        if dirpath == name:
            if not file.endswith('.py'):  # 不取py文件，因为python文件不是其他资源，是程序
                resources.append(file)
        else:
            basepath = dirpath.split(os.path.sep, 1)[1]
            resources.append(os.path.join(basepath, file))

setup(name=name,
      version=__version__,
      description='faster http/1.1 client than requests',
      author='Sheng Fan',
      author_email='1175882937@qq.com',
      url='https://github.com/fred913/sockethttp',
      packages=['sockethttp'],
      long_description="faster http/1.1 client than requests. \n"
      "Supported methods: GET and POST",
      license="GPL-2.0",
      platforms=["any"],
      python_requires=">=2.7")
