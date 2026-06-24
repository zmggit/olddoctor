# collect/tongue/tongue_detector.py
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image

### 负责加载模型和检测舌头。
class TongueDetector:
    def __init__(self, weights_path: str = "collect/tongue/weights/tongue_detector.pt"):
        """
        初始化舌头检测器。
        Args:
            weights_path (str): 预训练权重文件的路径。
        """
        # 这里可以替换为你自己训练或找到的舌体检测权重
        self.model = YOLO(weights_path)
        self.conf_threshold = 0.5  # 置信度阈值，低于此值视为未检测到

    def detect(self, image: Image.Image):
        """
        检测图片中的舌头。
        Args:
            image (PIL.Image): 输入的PIL图像。
        Returns:
            tuple: (是否检测到舌头, 裁剪后的舌头图像, 检测置信度)
        """
        # 将PIL图像转换为OpenCV格式 (YOLO可以直接接受PIL，但为了裁剪方便，这里转换)
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB_BGR)

        # 执行推理
        results = self.model(img_cv, conf=self.conf_threshold)

        # 解析结果
        for result in results:
            boxes = result.boxes
            if boxes is not None and len(boxes) > 0:
                # 取置信度最高的第一个检测框
                box = boxes[0]
                conf = box.conf.item()
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                # 裁剪舌头区域，并添加边界保护
                h, w = img_cv.shape[:2]
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)

                if x2 > x1 and y2 > y1:
                    tongue_crop = img_cv[y1:y2, x1:x2]
                    # 将裁剪后的图像转换回PIL格式，以兼容你的分类器
                    tongue_pil = Image.fromarray(cv2.cvtColor(tongue_crop, cv2.COLOR_BGR2RGB))
                    return True, tongue_pil, conf
                else:
                    return False, None, 0.0

        # 未检测到舌头
        return False, None, 0.0