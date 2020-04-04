# coding: utf-8

from __future__ import absolute_import
import importlib
from .request import request
from .get import get
from .post import post
from os.path import abspath, join, dirname
from io import open
from json import load as load_json
from .__init__ import __version__
from pip._internal import main
import importlib


def missing_module(module_name):
    print("Required module %s not detected, installing with pip..." %
          (module_name, ))
    main.main(["install", module_name])


def load_extension(extension_name):
    json_file = open(join(dirname(__file__), "extensions", extension_name,
                          "ext.json"),
                     "r",
                     encoding="utf-8")
    extension_info = load_json(json_file)
    json_file.close()
    globals_env = {
        "run_in_sockethttp": True,
        "sockethttp_version": __version__,
        "request": request,
        "get": get,
        "post": post
    }
    for i in extension_info['requires']:
        try:
            globals_env[i] = importlib.import_module(i)
        except ImportError:
            missing_module(i)
            globals_env[i] = importlib.import_module(i)
    for i in extension_info["extfiles"]:
        globals_env[i] = open(
            join(dirname(__file__), "extensions", extension_name,
                 extension_info['extfiles'][0][0]),
            *extension_info['extfiles'][0][1:],
            **extension_info['extfiles'][1])
    locals_env = {}
    extension_script = open(join(dirname(__file__), "extensions",
                                 extension_name, "ext.py"),
                            "r",
                            encoding="utf-8")
    exec(compile(
        "\n".join([(i if "# DELETELINE" not in i else "")
                   for i in extension_script.readlines()]),
        "<sockethttp extension>", "exec"),
         locals=locals_env,
         globals=globals_env)
    return locals_env['ext'] or globals_env['ext']
