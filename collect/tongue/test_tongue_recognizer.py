import os
import sys
import torch
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from collect.tongue.tongue_recognizer import TCMTongueRecognizer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def test_env():

    print(torch.backends.mps.is_available(),"环境")
    print(torch.backends.mps.is_built(),"环境")

def test_analyze_tongue():
    image_path = os.path.join(BASE_DIR, "data", "test", "no1.jpg")
    recognizer = TCMTongueRecognizer()
    result = recognizer.analyze(image_path)

    print(result["tongue_description"])
    assert "tongue_description" in result
    assert isinstance(result["success"], bool)


if __name__ == "__main__":
    test_analyze_tongue()