from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import hashlib
import os


class TCMTongueRecognizer:
    def __init__(self):
        # 假设你以后自己微调了一个模型并放在了本地的 "./models/tcm-tongue-model"
        # 你的本地模型应该配置了 id2label，例如：
        # {0: "舌色-淡红", 1: "舌色-红", 2: "苔色-白", 3: "苔色-黄", 4: "舌形-齿痕", 5: "苔质-厚腻"}


        self.model_name = "facebook/convnext-base-224"  # 目前暂用通用模型占位

        self.processor = AutoImageProcessor.from_pretrained(self.model_name)
        self.model = AutoModelForImageClassification.from_pretrained(self.model_name)
        self.model.eval()

    def crop_tongue(self, image: Image.Image) -> Image.Image:
        """
        [非常重要的一步]
        未来这里应该接入一个 YOLO 模型（如 YOLOv8），专门识别舌头边界框 (Bounding Box)
        并把舌头区域裁剪出来。目前为了跑通，直接返回原图。
        """
        # TODO: Implement YOLOv8 tongue detection and cropping
        return image

    def analyze(self, image_path: str) -> dict:
        if not os.path.exists(image_path):
            return {"error": "图片不存在"}

        with open(image_path, "rb") as f:
            img_hash = hashlib.md5(f.read()).hexdigest()

        original_image = Image.open(image_path).convert("RGB")

        # 1. 预处理：只保留舌体部分
        tongue_image = self.crop_tongue(original_image)

        inputs = self.processor(images=tongue_image, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits

            # [改造点]：真正的舌诊通常是多标签预测，这里假设用 sigmoid 替代 softmax
            # probs = torch.nn.functional.sigmoid(logits)
            # top_indices = torch.where(probs > 0.5)[1].tolist()

            # 暂用单分类演示
            probs = torch.nn.functional.softmax(logits, dim=-1)
            predicted_id = probs.argmax(-1).item()
            confidence = probs[0][predicted_id].item()

        # 如果是通用模型，出来的还是 ImageNet 标签；
        # 如果是你微调的模型，出来的将是 "黄厚腻苔, 齿痕舌"
        raw_label = self.model.config.id2label.get(predicted_id, f"class_{predicted_id}")

        return {
            "analysis": {
                "tongue_body_color": "未知",  # 待专科模型补充
                "coating_color": "未知",  # 待专科模型补充
                "coating_nature": "未知",  # 待专科模型补充
                "tongue_shape": "未知",  # 待专科模型补充
            },
            "raw_model_output": raw_label,
            "confidence": confidence,
            "image_hash": img_hash,
            "disclaimer": "AI舌诊仅供参考，不作为最终医疗诊断依据。请结合中医四诊合参。"
        }