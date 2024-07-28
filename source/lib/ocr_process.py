import os
import time
import cv2
import json
import easyocr

ocr_json_folder = "/Users/apple/Desktop/Python/Smarcle/PythonWeek/Notion/asset/json"
text_save_folder = "/Users/apple/Desktop/Python/Smarcle/PythonWeek/Notion/asset/texts"

# 디렉토리 생성
os.makedirs(ocr_json_folder, exist_ok=True)
os.makedirs(text_save_folder, exist_ok=True)

ocr_model = easyocr.Reader(['ko', 'en'], gpu=True)

def load_ocr_results():
    ocr_results_path = os.path.join(ocr_json_folder, "ocr_results.json")
    if os.path.exists(ocr_results_path):
        with open(ocr_results_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    return {}

def save_ocr_results(ocr_results):
    ocr_results_path = os.path.join(ocr_json_folder, "ocr_results.json")
    with open(ocr_results_path, "w", encoding="utf-8") as json_file:
        json.dump(ocr_results, json_file, ensure_ascii=False, indent=4)

def save_individual_ocr_result(timestamp, result):
    individual_ocr_path = os.path.join(ocr_json_folder, f"{timestamp}.json")
    with open(individual_ocr_path, "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, ensure_ascii=False, separators=(',', ':'))

def convert_to_serializable(result):
    """
    Convert OCR result to a JSON serializable format with no line breaks for bbox.
    """
    serializable_result = []
    for item in result:
        serializable_item = {
            "bbox": [list(map(float, point)) for point in item[0]],  # numpy 배열을 float 리스트로 변환
            "text": item[1],
            "prob": float(item[2])
        }
        serializable_result.append(serializable_item)
    return serializable_result

def extract_text_from_image(screenshot_queue, processed_queue):
    ocr_results = load_ocr_results()
    while True:
        screenshot_path, timestamp = screenshot_queue.get()
        image = cv2.imread(screenshot_path)
        image = cv2.resize(image, (1920, 1080))  # 이미지 해상도를 1920x1080으로 규격화
        result = ocr_model.readtext(image, batch_size=16)  # Batch size를 16으로 설정하여 속도 향상
        serializable_result = convert_to_serializable(result)

        # 결과 저장
        ocr_results[timestamp] = [item["text"] for item in serializable_result]
        save_ocr_results(ocr_results)

        # 개별 JSON 파일로 저장
        individual_result = {
            "time": timestamp.replace("_", "")[2:],
            "value": serializable_result
        }
        save_individual_ocr_result(timestamp, individual_result)

        text = "\n".join([detection["text"] for detection in serializable_result])
        processed_queue.put((screenshot_path, text, timestamp))
        screenshot_queue.task_done()

        # 추출한 텍스트 저장
        with open(os.path.join(text_save_folder, f"text_{timestamp}.txt"), "w", encoding="utf-8") as f:
            f.write(f"[OCR 결과]\n{text}")

