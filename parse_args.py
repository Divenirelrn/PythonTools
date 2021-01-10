import argparse


def args_parse():
    parser = argparse.ArgumentParser(description="YOLOV3 args")

    parser.add_argument("--image", default="./dog-cycle-car.png", help="Path of image/directory")
    parser.add_argument('--save_path', help='save path', default='./results')
    parser.add_argument('--cfg', help='cfg_path', default='./yolov3.cfg')
    parser.add_argument('--weights', help='weights path', default='./yolov3.weights')
    parser.add_argument('--input_size', help='input size', default=416)
    parser.add_argument('--batch_size', default=2)
    parser.add_argument('--confidence', help='confidence to filter detections', default=0.5)
    parser.add_argument('--nms_conf', help='threshhold fpr nms', default=0.4)

    return parser.parse_args()