# search_process.py
import os
import json

ocr_json_path = "/Users/apple/Desktop/Python/Smarcle/PythonWeek/Notion/asset/json/ocr_results.json"

def load_ocr_results():
    if os.path.exists(ocr_json_path):
        with open(ocr_json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    return {}

def search_keyword_in_ocr(keyword):
    ocr_results = load_ocr_results()
    matching_timestamps = []

    for timestamp, texts in ocr_results.items():
        if any(keyword in text for text in texts):
            matching_timestamps.append(timestamp)
    
    return matching_timestamps
