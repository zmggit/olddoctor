from PIL import Image
import torch
from transformers import AutoModelForImageClassification, AutoImageProcessor
import os


class TongueRecognizer:
    def __init__(self):
        # 使用一个开源的中医舌诊相关模型（可替换为更强的本地模型）
        self.model_name = "Qunmasj-Vision-Studio/tongue-classification"  # 示例开源模型
        self.processor = AutoImageProcessor.from_pretrained(self.model_name)
        self.model = AutoModelForImageClassification.from_pretrained(self.model_name)
        self.model.eval()

    def analyze_tongue(self, image_path: str) -> str:
        """分析舌苔图片并返回文本描述"""
        try:
            image = Image.open(image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt")

            with torch.no_grad():
                outputs = self.model(**inputs)
                predicted_class = outputs.logits.argmax(-1).item()
                confidence = torch.softmax(outputs.logits, dim=-1)[0][predicted_class].item()

            # 标签映射（根据实际模型调整）
            labels = {
                0: "舌质淡红，苔薄白",
                1: "舌红苔黄厚腻",
                2: "舌淡胖有齿痕，苔白滑",
                3: "舌紫暗有瘀点",
                4: "舌红无苔或少苔",
                # ... 可继续扩展
            }

            description = labels.get(predicted_class, "舌象特征异常")
            return f"{description}（置信度: {confidence:.2%}）"

        except Exception as e:
            return f"舌苔图片分析失败: {str(e)}"


# 单例
tongue_analyzer = TongueRecognizer()