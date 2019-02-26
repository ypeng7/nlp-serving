# -*- coding:utf-8 -*-
"""
# @file: abstract_inference_service.py
#
# @date: 01/15/2019, 17:35:07
# @author: Yue Peng
# @email: yuepaang@gmail.com
#
# @brief:
#
# @detail:
"""
__author__ = "Yue Peng"

from abc import ABCMeta, abstractmethod


class AbstractInferenceService(object):
    """
    The abstract class for inference service which should implement the method.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self.model_name = None
        self.model_base_path = ""
        self.model_version_list = []
        self.model_graph_signature = None
        self.model_graph_signature_dict = {}
        self.platform = ""

    @abstractmethod
    def inference(self, json_data):
        pass

    def get_details(self):
        details = {}
        details["model_name"] = self.model_name
        details["model_base_path"] = self.model_base_path
        details["model_version_list"] = self.model_version_list
        details["model_signature"] = self.model_graph_signature_dict
        details["platform"] = self.platform
        return details

