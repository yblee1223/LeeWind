# ocr_process.py
import os
import time
import cv2
import json
import easyocr

ocr_json_folder = "/Users/apple/Desktop/Python/Smarcle/PythonWeek/Notion/asset/json"
ocr_json_path = os.path.join(ocr_json_folder, "ocr_results.json")
text_save_folder = "/Users/apple/Desktop/Python/Smarcle/PythonWeek/Notion/asset/texts"

# 디렉토리 생성
os.makedirs(ocr_json_folder, exist_ok=True)
os.makedirs(text_save_folder, exist_ok=True)

ocr_model = easyocr.Reader(['ko', 'en'], gpu=True)

def load_ocr_results():
    if os.path.exists(ocr_json_path):
        with open(ocr_json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    return {}

def save_ocr_results(ocr_results):
    with open(ocr_json_path, "w", encoding="utf-8") as json_file:
        json.dump(ocr_results, json_file, ensure_ascii=False, indent=4)

def extract_text_from_image(screenshot_queue, processed_queue):
    ocr_results = load_ocr_results()
    while True:
        screenshot_path, timestamp = screenshot_queue.get()
        image = cv2.imread(screenshot_path)
        image = cv2.resize(image, (1920, 1080))  # 이미지 해상도를 1920x1080으로 규격화
        result = ocr_model.readtext(image, batch_size=16)  # Batch size를 16으로 설정하여 속도 향상

        # 텍스트 추출
        text_list = [detection[1] for detection in result]

        # 결과 저장
        ocr_results[timestamp] = text_list
        save_ocr_results(ocr_results)

        joined_text = "\n".join(text_list)
        processed_queue.put((screenshot_path, joined_text, timestamp))
        screenshot_queue.task_done()

        # 추출한 텍스트 저장
        with open(os.path.join(text_save_folder, f"text_{timestamp}.txt"), "w", encoding="utf-8") as f:
            f.write(f"[OCR 결과]\n{joined_text}")
