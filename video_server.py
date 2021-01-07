#import torch.multiprocessing as mp
import multiprocessing as mp
import time
import cv2
import datetime

import threading
import torch
from vgg import vgg19
from torchvision import transforms
from PIL import Image
import requests
import json

trans = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

model = vgg19()
model.load_state_dict(torch.load('best_model.pth', map_location=torch.device('cpu')))
url = 'https://5gvr.komect.com/edu/stu-flow'#"http://117.139.13.88:18089/scenic/bsdFlow"
rtmp_str = 'rtmp://47.106.60.245:1936/live/620271123-1?eyJrZXkiOjAsInNpZ24iOiJFZ2FSYjhpdC1mMW5EbHJxb19WQWdmVEYza3FUQmZmZy1kOW53SGJrYVA2V3E5T1hCMFdmd0NXc1hscktsX0hwTnpnU2NtNTNKSWRCemZQdWN3RGtsbHdtQVUzWk9zU0t5NG1OekdGNnplUXJsRVoxSGktMTJFMnNNZUpDUUg1dGVvamdNY3NKdlJ1b1ZRT1cyaF9OSWdPUUt6YTlwREFzVEU1Q0tTOGlkTWMifQ'
def queue_img_put(q, name, pwd, ip, channel=1):
    cap = cv2.VideoCapture(rtmp_str)
    while True:
        is_opened, frame = cap.read()
        q.put(frame) if is_opened else None
        q.get() if q.qsize() > 1 else None
        # if is_opened:
        #     q.put(frame)
        # else:
        #     continue
        #
        # if q.qsize() > 1:
        #     q.get()
        # else:
        #     continue

def queue_img_get(q, window_name):
    i = 0
    while True:
        frame = q.get()
        print(frame)
        #if frame.shape and frame.shape[-1] == 3:
        i = i + 1
        print('i=', i)
        x, y = frame.shape[0:2]
        image = cv2.resize(frame, (int(y / 2), int(x / 2)))
        image_path = './data_people/' + str(i) + '.jpg'
        print(image_path)
        cv2.imwrite(image_path, image)
        img = Image.open(image_path).convert('RGB')
        img = trans(img).unsqueeze(0)
        inputs = img
        assert inputs.size(0) == 1, 'the batch size should equal to 1'
        with torch.set_grad_enabled(False):
            outputs = model(inputs)
            temp_minu = torch.sum(outputs).item()
            print(torch.sum(outputs).item())
        data = {}
        data['log_id'] = '12'
        data['camera_id'] = '620271118'
        data['time'] = str(datetime.datetime.now())[:-7]
        # print(str(datetime.datetime.now())[:-8])
        data['person_num'] = str(int(temp_minu))
        payload = json.dumps(data)
        # payload = "{\"log_id\": \"12\",\"camera_id\": \"01\",\"time\": \"2020-08-22-12:02:30\",\"person_num\": \"3\"}"
        headers = {'Content-Type': 'application/json'}

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))
        # else:
        #     continue


def run():
    user_name, user_pwd, camera_ip = "admin", "password", "192.168.1.164"

    mp.set_start_method(method='spawn')  # multi-processing init
    queue = mp.Queue(maxsize=2)
    processes = [mp.Process(target=queue_img_put, args=(queue, user_name, user_pwd, camera_ip)),
                 mp.Process(target=queue_img_get, args=(queue, camera_ip))]

    [setattr(process, "daemon", True) for process in processes]  # process.daemon = True
    [process.start() for process in processes]
    [process.join() for process in processes]


if __name__ == '__main__':
    run()
pass
