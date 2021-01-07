#######导入网络请求模块########
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tornado.web
from tornado import gen
from tornado.httpserver import HTTPServer
import json
import tornado.options
import logging
from tornado.web import RequestHandler
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.escape import json_decode, json_encode
import base64
#######导入逻辑模块############
import os
import time
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
#######导入检测模块############
from utils import Detector
from configs import FLAGS
from category import clsid2catid, id2name

#网络请求相关方法
def call_result(result_code, result_data, error_state='错误'):
    json_result = {}
    json_result["result_code"] = result_code
    json_result["result_msg"] = error_state
    json_result["result_data"] = result_data
    logging.info(json_result)
    return json_result
#初始化检测模型
detector = Detector(
    FLAGS.model_dir, use_gpu=FLAGS.use_gpu, run_mode=FLAGS.run_mode)

class Object_DetectionHandler(RequestHandler):
    # xecutor = ThreadPoolExecutor(1)
    # run_on_executor
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        request_result = {}
        try:
            senceinfo_dict = json.loads(self.request.body)
        except Exception as e:
            logging.info({"message": e})
            senceinfo_dict = dict()
        if len(senceinfo_dict.keys()) < 1:
            result = call_result('50002', request_result, '请求参数缺失')
            return self.write(json_encode(result))

        try:
            img_data_base64 = senceinfo_dict.get("image")
        except:
            return self.write(json_encode(call_result('50001', request_result, '请求参数错误1')))

        if img_data_base64 is None:
            return self.write(json_encode(call_result('50001', request_result, '请求参数错误3')))
        try:
            img_data = base64.b64decode(img_data_base64)
        except:
            return self.write(json_encode(call_result('50004', request_result, '图像数据解码失败')))
        try:
            ############ save imgs############
            file_root = '/home/api_serves/object_detection/deploy/python/detect_imgs'
            img_name = os.path.join(file_root, 'detect_img.jpg')
            file = open(img_name, 'wb')
            file.write(img_data)
            file.close()
            ##################picture classify##################
            start = time.time()
            res = detector.predict(img_name, FLAGS.threshold)
            end = time.time()
            print('predict time:', end - start)
            recg_resut_final = []
            for obj in res['boxes']:
                 temp = {}
                 temp['score'] = round(float(obj[1]), 2)
                 temp['classify_name'] = id2name[clsid2catid[int(obj[0])]]
                 temp['location'] = [round(float(obj[2]), 2), round(float(obj[3]), 2), round(float(obj[4]), 2), round(float(obj[5]), 2)]
                 if temp['score'] >= 0.5:
                     recg_resut_final.append(temp)
            request_result['detections'] = recg_resut_final
            return self.write(json.dumps(call_result('50000', request_result, '正确'), ensure_ascii=False))
        except Exception as e:
            return self.write(json_encode(call_result('50006', request_result, '算法内部错误，请联系算法人员')))

def make_app():
    return tornado.web.Application([
        (r"/object_detection", Object_DetectionHandler),
    ])

def main():
    app = make_app()
    server = HTTPServer(app)
    server.bind(1443)
    server.start(1)  # 设置启动多少个进�?
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
