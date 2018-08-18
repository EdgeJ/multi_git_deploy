import json
import glob
import requests_mock

adapter = requests_mock.Adapter()
mock_json = {}

for json_file in glob.glob('*.json'):
    with open(json_file) as f:
        mock_json[json_file.split('.')[0]] = json.loads(f.read())

adapter.register_uri(
    'GET',
    'mock://gitlab/projects',
    json=mock_json['projects'],
    status_code=200
)

adapter.register_uri(
    'GET',
    'mock://gitlab/projects/4',
    json=mock_json['projects'][0],
    status_code=200
)

adapter.register_uri(
    'GET',
    'mock://gitlab/projects/4/repository/branches',
    json=mock_json['branches'],
    status_code=200
)

adapter.register_uri(
    'GET',
    'mock://gitlab/projects/1/merge_requests/1',
    json=mock_json['merge_request'],
    status_code=200
)

adapter.register_uri(
    'GET',
    'mock://gitlab/projects/1/merge_requests/1/changes',
    json=mock_json['merge_changes'],
    status_code=200,
)

# results for success (200), no permission (401), conflicts (405), and already
# closed (406)
for key, val in {1: 200, 2: 401, 3: 405, 4: 406}.items():
    adapter.register_uri(
        'PUT',
        'mock://gitlab/projects/1/merge_requests/{}/merge'.format(key),
        json=mock_json['merge_accept'],
        status_code=val
    )
