# -*- coding:utf-8 -*-
"""
# @file: marshal_util.py
#
# @date: 01/15/2019, 22:17:14
# @author: Yue Peng
# @email: yuepaang@gmail.com
#
# @brief:
#
# @detail:
"""
__author__ = "Yue Peng"

from hashlib import md5

import marshal
import types

__all__ = ["FuncMarshal"]


class FuncMarshal(object):

    @classmethod
    def md5sum(cls, serialized):
        hasher = md5()
        hasher.update(serialized)
        return hasher.hexdigest()

    @classmethod
    def serialize(cls, function, file_path):
        if callable(function):
            serialized = marshal.dumps(function.__code__)
            with open(file_path, "wb") as f:
                marshal.dump(function.__code__, f)
            # print("The md5 of function %s is %s, please record it to your json file." %(function.__name__, cls.md5sum(serialized)))
            print(f"The md5 of function {function.__name__} "
            f"is {cls.md5sum(serialized)}, please record it to your json file.")
            return (cls.md5sum(serialized), serialized)

    @classmethod
    def deserialize(cls, file_path):
        serialized = open(file_path, "rb").read()
        code = marshal.load(open(file_path, "rb"))

        return (cls.md5sum(serialized), types.FunctionType(code, globals()))

