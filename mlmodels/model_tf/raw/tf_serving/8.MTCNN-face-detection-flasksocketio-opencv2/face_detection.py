import time

import cv2
import visualization_utils
from Detection.detector import Detector
from Detection.fcn_detector import FcnDetector
from Detection.MtcnnDetector import MtcnnDetector
from train_models.mtcnn_model import O_Net, P_Net, R_Net

thresh = [0.7, 0.1, 0.1]
min_face_size = 24
stride = 2
slide_window = True
shuffle = False
detectors = [None, None, None]
prefix = [
    "data/MTCNN_model/PNet_landmark/PNet",
    "data/MTCNN_model/RNet_landmark/RNet",
    "data/MTCNN_model/ONet_landmark/ONet",
]
epoch = [18, 14, 16]
model_path = ["%s-%s" % (x, y) for x, y in zip(prefix, epoch)]
PNet = FcnDetector(P_Net, model_path[0])
detectors[0] = PNet
RNet = Detector(R_Net, 24, 1, model_path[1])
detectors[1] = RNet
ONet = Detector(O_Net, 48, 1, model_path[2])
detectors[2] = ONet
mtcnn_detector = MtcnnDetector(
    detectors=detectors,
    min_face_size=min_face_size,
    stride=stride,
    threshold=thresh,
    slide_window=slide_window,
)


def detect_face(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes_c, _ = mtcnn_detector.detect(img)
    for i in range(boxes_c.shape[0]):
        bbox = boxes_c[i, :4]
        visualization_utils.draw_bounding_box_on_image_array(
            img_rgb,
            int(bbox[1]),
            int(bbox[0]),
            int(bbox[3]),
            int(bbox[2]),
            "YellowGreen",
            display_str_list=["face"],
            use_normalized_coordinates=False,
        )
    return img_rgb
