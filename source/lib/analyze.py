# analyze.py
import os
import time
import json
from PIL import Image

ocr_json_path = "/Users/apple/Desktop/Python/Smarcle/PythonWeek/Notion/asset/json/ocr_results.json"

def load_ocr_results():
    if os.path.exists(ocr_json_path):
        with open(ocr_json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    return {}

def analyze_screenshot(screenshot_list, N):
    ocr_results = load_ocr_results()
    current_time = time.time()
    target_time = current_time - N
    
    for screenshot_path, text, timestamp in reversed(screenshot_list):
        screenshot_time = time.mktime(time.strptime(timestamp, "%Y_%m_%d_%H_%M_%S"))
        if screenshot_time <= target_time:
            image = Image.open(screenshot_path)
            image.show()  # 스크린샷을 화면에 표시합니다
            if timestamp in ocr_results:
                ocr_text_list = ocr_results[timestamp]
                ocr_text = "\n".join(ocr_text_list)
                print(f"[OCR 결과]\n'{ocr_text}'")  # 텍스트 출력
            else:
                print(f"No OCR results found for timestamp {timestamp}")
            return

    print(f"No screenshot found for {N} seconds ago.")
