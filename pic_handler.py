import requests
import base64

from const import key_list


TOKEN = None
failed_key_list = []


def get_key():
    for key in key_list:
        if key not in failed_key_list:
            return key
    return None


def get_token(key):
    api_key = key["api_key"]
    secret_key = key["secret_key"]
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'\
        .format(api_key, secret_key)
    response = requests.get(host)
    token = None
    if response:
        res: dict = response.json()
        token = res.get("access_token")
    return token


def pic_handle(pic_url, key):
    '''
    通用文字识别（高精度版）
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open(pic_url, 'rb')
    img = base64.b64encode(f.read())

    global TOKEN
    if not TOKEN:
        TOKEN = get_token(key)
    request_url = request_url + "?access_token=" + TOKEN
    params = {"image": img, "paragraph": False}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    res = {}
    if response:
        res: dict = response.json()
        new_key = key_failed(res, key)
        if new_key:
            count = 0
            if count < 1:
                res = pic_handle(pic_url, new_key)
            else:
                res = {}
    return res


def key_failed(res, key):  # TODO TOKEN
    new_key = False
    if res.get("error_code"):
        failed_key_list.append(key)
        new_key = get_key()
    return new_key
