# -*- coding:utf-8 -*-
"""
# @file: sklearn.py
#
# @date: 01/25/2019, 10:48:10
# @author: Yue Peng
# @email: yuepaang@gmail.com
#
# @brief: The ``nlp_serving.sklearn`` module provides an API for logging and loading scikit-learn models
#
# @detail:
"""
__author__ = "Yue Peng"

import os
import pickle
# import yaml
# import copy

# import sklearn
from sklearn.externals.joblib import dump, load

FLAVOR_NAME = "sklearn"

SERIALIZATION_FORMAT_JOBLIB = "joblib"
SERIALIZATION_FORMAT_PICKLE = "pickle"

SUPPORTED_SERIALIZATION_FORMAT = [
    SERIALIZATION_FORMAT_JOBLIB
]


def save_model(
        sk_model,
        path,
        serialization_format=SERIALIZATION_FORMAT_JOBLIB
        ):
    if serialization_format not in SUPPORTED_SERIALIZATION_FORMAT:
        raise ValueError(
            f"Unrecognized serialization format: {serialization_format}. "
            f"Please specify one of the following supported formats: "
            f"{SUPPORTED_SERIALIZATION_FORMAT}."
        )

    if os.path.exists(path):
        raise ValueError(
            f"Path '{path}' already exists"
        )
    os.makedirs(path)
    if serialization_format == SERIALIZATION_FORMAT_PICKLE:
        model_data_subpath = "model.pkl"
    elif serialization_format == SERIALIZATION_FORMAT_JOBLIB:
        model_data_subpath = "model.joblib"

    _save_model(
        sk_model=sk_model,
        output_path=os.path.join(path, model_data_subpath),
        serialization_format=serialization_format
    )


def _save_model(sk_model, output_path, serialization_format):
    with open(output_path, "wb") as out:
        if serialization_format == SERIALIZATION_FORMAT_PICKLE:
            pickle.dump(sk_model, out)
        elif serialization_format == SERIALIZATION_FORMAT_JOBLIB:
            dump(sk_model, out)
        else:
            raise ValueError(
                f"Unrecognized serialization format: {serialization_format}. "
                f"Please specify one of the following supported formats: "
                f"{SUPPORTED_SERIALIZATION_FORMAT}."
            )

