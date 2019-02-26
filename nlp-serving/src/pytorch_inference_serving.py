# -*- coding:utf-8 -*-
"""
# @file: pytorch_inference_serving.py
#
# @date: 01/16/2019, 16:39:45
# @author: Yue Peng
# @email: yuepaang@gmail.com
#
# @brief:
#
# @detail:
"""
__author__ = "Yue Peng"

import os
import pytorch


STATE_DICT_NAME = os.environ["STATE_DICT_NAME"]


class SetupModel(object):
    model = Model()

    def __init__(self, func):
        self.func = func
        state_dict = torch.load(STATE_DICT_NAME, map_location=lambda storage, loc: storage)
        self.model.load_state_dict(state_dict), self.model.eval()

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
