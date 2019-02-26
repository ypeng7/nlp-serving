# -*- coding:utf-8 -*-
"""
# @file: helper.py
#
# @date: 01/21/2019, 11:16:41
# @author: Yue Peng
# @email: yuepaang@gmail.com
#
# @brief:
#
# @detail:
"""
__author__ = "Yue Peng"

# import argparse
import logging
# import uuid


def set_logger(context, verbose=False):
    logger = logging.getLogger(context)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    formatter = logging.Formatter(
            "%(levelname)-.1s:" +
            context +
            ":[%(filename).3s:%(funcName).3s:%(lineno)3d]:%(message)s",
            datefmt="%m-%d %H:%M:%S")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(console_handler)
    return logger

