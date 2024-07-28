import PIL.Image
import pyautogui
import os
import easyocr
import time
import numpy as np
import json
import cv2
import threading
import PIL
import sys

sys.path.append(os.path.join(os.getcwd(), 'src'))
from lib.utils import get_active_window_info, get_filename

class OCR:
    def __init__(self):
        self.save_folder = 'data/jsons'
        os.makedirs(self.save_folder, exist_ok=True)  
        self.model = easyocr.Reader(['ko', 'en'], gpu=True)

    def process(self, img, file_name, programe_name):
        thread = threading.Thread(target=self.extract_OCR, args=(self.model, img, file_name, programe_name))
        thread.start()

    def save_json(self, result, file_name, programe_name):
        path = os.path.join(self.save_folder, f"ocr_{file_name}.json")
        file = { 
                "program" : programe_name,
                "value" : result
                }
        with open(path, "w", encoding="utf-8") as json_file:
            json.dump(file, json_file, ensure_ascii=False, indent=4)
    
    def save_text():
        pass

    def extract_OCR(self, model, img, file_name, programe_name):
        result = model.readtext(img, batch_size=16)
        result = self.convert_to_serializable(result)
        self.save_json(result, file_name, programe_name)
    
    def convert_to_serializable(self, result, ):
        serializable_result = []  
        for item in result:
            serializable_item = {
                "bbox": [list(map(float, point)) for point in item[0]],  # numpy 배열을 float 리스트로 변환
                "text": item[1],  
                "prob": float(item[2])  
            }
            serializable_result.append(serializable_item)  
        return serializable_result  # 직렬화 가능한 결과 리스트 반환

class Capture:
    def __init__(self):
        self.__running = False
        self.save_folder = 'data/screenshots'
        os.makedirs(self.save_folder, exist_ok=True)
        self.OCR = OCR()

    def _screen_capture(self, gap : int=60, size=None):
        while self.__running:
            img = pyautogui.screenshot()
            file_name = get_filename()
            programe_name = get_active_window_info()
            self.OCR.process(np.array(img), file_name, programe_name)
            if size is not None:
                img = np.array(img)
                img = cv2.resize(img, size)
                img = PIL.Image(img)
            # save_img
            path = os.path.join(self.save_folder, f"screenshots_{file_name}.png")
            img.save(path)
            time.sleep(gap)
    
    def start_screenshot(self):
        self.__running = True
        thread = threading.Thread(target=self._screen_capture, args=(1, None))
        thread.start()
    
    def stop_screenshot(self):
        self.__running = False
        print("---screenshot end---")



def capture_demo():
    capture = Capture()
    capture.start_screenshot()
    time.sleep(10)
    capture.stop_screenshot()

def ocr_demo():
    model = OCR()
    img1 = "data/screenshots/screenshots_2024_07_28_16_16_51.png"
    img2 = "data/screenshots/screenshots_2024_07_28_16_17_40.png"
    model.process(img1, get_filename())
    model.process(img2, get_filename())

if __name__ == "__main__":
    capture_demo()
    # ocr_demo()