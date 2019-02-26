# -*- coding:utf-8 -*-
import yaml
from datetime import datetime
"""
# @file: sklearn_inference_service.py
#
# @date: 01/15/2019, 17:41:31
# @author: Yue Peng
# @email: yuepaang@gmail.com
#
# @brief:
#
# @detail:
"""
__author__ = "Yue Peng"

import os
import logging
import time
import numpy as np
import ujson as json

from abstract_inference_service import AbstractInferenceService
from marshal_util import FuncMarshal

logger = logging.getLogger("nlp-serving")
logger.setLevel(logging.WARNING)


class SklearnInferenceService(AbstractInferenceService):
    def __init__(self, model_name, model_base_path, json_path):
        super(SklearnInferenceService, self).__init__()

        self.model_name = model_name
        self.model_base_path = model_base_path
        # change working directory to model folder
        os.chdir(os.path.dirname(self.model_base_path))
        self.model_version_list = []
        self.model_graph_signature = ""
        self.platform = "sklearn"

        # Loading your json configuration file
        with open(json_path, "r") as f:
            self.json_data = json.load(f)

        self.model_version_list.append(str(self.json_data["version"]))

        if self.model_base_path.endswith(".joblib"):
            from sklearn.externals import joblib
            import warnings
            warnings.filterwarnings("ignore")
            self.pipeline = joblib.load(self.model_base_path)
        elif (self.model_base_path.endswith(".pickle") or
                model_base_path.endswith(".pkl")):
            import pickle
            with open(self.model_base_path, "r") as f:
                self.pipeline = pickle.load(f)
        else:
            logger.error(
                "Unsupported model file format: {}".format(
                    self.model_base_path),
                exc_info=True)

        if hasattr(self.pipeline, "get_params"):
            self.model_graph_signature = str(self.pipeline.get_params())
        else:
            logger.warn("Model object has not get_params method.")

    def inference(self, sentence):

        # Preprocess function transform string to numpy
        if self.json_data.get("preprocess_md5", "NULL") != "NULL":
            preprocess_md5, preprocess_function = FuncMarshal.deserialize(
                self.json_data["preprocess_marshal"])
            if preprocess_md5 == self.json_data["preprocess_md5"]:
                input_data = preprocess_function(sentence)
                logger.debug(
                    "Preprocess to generate data: {}".format(
                        input_data))
            else:
                logger.warn("md5 does not match.")

        if not isinstance(input_data, np.ndarray):
            request_ndarray_data = np.array(input_data)
        else:
            request_ndarray_data = input_data

        # Inference
        if self.json_data.get("inference_md5", "NULL") != "NULL":
            start_time = time.time()
            inference_md5, inference_function = FuncMarshal.deserialize(
                self.json_data["inference_marshal"])
            if inference_md5 == self.json_data["inference_md5"]:
                prediction = inference_function(
                    self.pipeline, request_ndarray_data)
                logger.debug(
                    "Inference time: {}".format(time.time() - start_time))
            else:
                logger.warn("md5 does not match.")

        result = {
            "prediction": prediction
        }

        logger.debug("Inference result: {}".format(result))

        return result


class Model(object):
    def __init__(
            self,
            artifact_path=None,
            run_id=None,
            time_created=datetime.now(),
            flavors=None
    ):
        # store model id instead of run_id
        # and path to avoid confusion when model gets exported
        if run_id:
            self.run_id = run_id
            self.artifact_path = artifact_path
        self.time_created = time_created.strftime("%Y-%m-%d %H:%M:%S")
        self.flavors = flavors if flavors is not None else {}

    def add_flavors(self, name, **params):
        self.flavors[name] = params
        return self

    def to_yaml(self, stream=None):
        return yaml.safe_dump(
            self.__dict__, stream=stream, default_flow_style=False)

    def save(self, path):
        with open(path, "w") as out:
            self.to_yaml(out)

    @classmethod
    def load(cls, path):
        with open(path) as f:
            return cls(**yaml.safe_load(f.read()))


if __name__ == "__main__":
    json_path = os.path.realpath("..") + "/models/lr/json_data.json"
    model_path = os.path.realpath(
        "..") + "/models/lr/model_lr_fengsheng_bot_714_20190109.joblib"
    sis = SklearnInferenceService(
        "fengbot",
        model_path, json_path)
    print(sis.inference("工资什么时候发？"))
    print(sis.model_graph_signature)
