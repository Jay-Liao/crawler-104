#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json


def save_dict_as_json_file(directory_path, filename, dict_data):
    file_path = os.path.join(directory_path, filename)
    with open(file_path, "w") as outfile:
        json.dump(dict_data, outfile)
