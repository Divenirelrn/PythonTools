import requests
import base64
import codecs
import sys
import os
from tqdm import tqdm

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=o3zrBIyAkM2gBc6OztUkdkMw&client_secret=1rBYD6pBsm78xLcepkdimI56Go6Ojp1p'
res = requests.get(host)
if res:
    access_token_getted = res.json()['access_token']
access_token = access_token_getted
headers = {'content-type': 'application/x-www-form-urlencoded'}
#with open('/home/data/train_places/multilabelTest/api/baidu/results/outputFir.txt', 'r', encoding='utf-8') as f:
#    lines = f.readlines()
#outList = [item.split(',')[0] for item in lines]
outList = []

# 二进制方式打开图片文件
def baiduAPI(img_dir):
    img_list = os.listdir(img_dir)
    with open('./results/special_baidu_4th.txt','w',encoding='utf-8') as fo:
        for imge in tqdm(img_list):
            if imge not in outList:
                string = imge + ','
                img_path = os.path.join(img_dir,imge)
                f = open(img_path, 'rb')
                img = base64.b64encode(f.read())
                params = {"image":img}
                request_url_new = request_url + "?access_token=" + access_token
                try:
                    response = requests.post(request_url_new, data=params, headers=headers, timeout=5)
                    if response:
                        results = response.json()
                        if results['result_num'] > 0:
                            for obj in results['result']:
                                string += obj['keyword'] + ':' + str(obj['score']) + ','
                    fo.write(string[:-1] + '\n')
                except:
                    fo.write(string[:-1] + '\n')
                    continue

if __name__ == '__main__':
    img_dir = '/home/data/train_places/multilabelTest/resources/special/Images_special_all'
    baiduAPI(img_dir)
