# -*- coding:utf-8 -*-
"""
# @file: freeze_tf_graph.py
#
# @date: 01/16/2019, 17:24:11
# @author: Yue Peng
# @email: yuepaang@gmail.com
#
# @brief:
#
# @detail:
"""
__author__ = "Yue Peng"

import os
import tensorflow as tf


def freeze_tf_graph(model_folder, output_node_names):
    files = os.listdir(model_folder)
    meta_file = [f for f in files if f.endswith(".meta")][0]
    meta_file_path = os.path.join(model_folder, meta_file)
    saver = tf.train.import_meta_graph(meta_file_path, clear_devices=True)
    graph = tf.get_default_graph()
    input_graph_def = graph.as_graph_def()
    sess = tf.Session()
    model_name = [f for f in files if f.endswith(".meta")][0].split(".")[0]
    print(model_name)
    saver.restore(sess, f"{model_folder}/{model_name}")

    output_graph_def = tf.graph_util.convert_variables_to_constants(
            sess,
            input_graph_def,
            output_node_names.split(",")
            )
    output_graph = f"{model_folder}/{model_name}.pb"
    with tf.gfile.GFile(output_graph, "wb") as f:
        f.write(output_graph_def.SerializeToString())
    sess.close()
