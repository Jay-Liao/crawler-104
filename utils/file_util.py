#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json


def save_dict_as_json_file(file_path, dict_data):
    with open(file_path, "w") as outfile:
        json.dump(dict_data, outfile)
