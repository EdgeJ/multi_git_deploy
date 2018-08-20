"""
Load json files representing Gitlab API response objects into a dict.
"""
import glob
import json
import os
import requests_mock

dir_path = os.path.dirname(os.path.realpath(__file__))
adapter = requests_mock.Adapter()
mock_json = {}

for json_file in glob.glob('{}/*.json'.format(dir_path)):
    with open(json_file) as f:
        mock_json[os.path.basename(json_file).split('.')[0]] = json.loads(f.read())
