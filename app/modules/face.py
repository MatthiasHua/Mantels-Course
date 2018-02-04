#人脸识别、比较

import requests
from json import JSONDecoder
from app import basepath

http_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"
key = "key"
secret = "secret"

def test_compare(filepath1, filepath2):
    filepath1 = basepath + filepath1
    filepath2 = basepath + filepath2

    data = {"api_key": key, "api_secret": secret}
    files = {"image_file1": open(filepath1, "rb"), "image_file2": open(filepath2, "rb")}
    response = requests.post(http_url, data=data, files=files)

    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)

    print(req_dict)

    print(req_dict['thresholds'])
    print(req_dict['confidence'])

    if req_dict['confidence'] > req_dict['thresholds']['1e-5']:
        print("是同一人")
        return 1
    elif req_dict['confidence'] > req_dict['thresholds']['1e-4']:
        print("可能性较高")
        return 2
    elif req_dict['confidence'] > req_dict['thresholds']['1e-3']:
        print("可能性不高")
        return 3
    else:
        print("不为同一人")
        return 4
