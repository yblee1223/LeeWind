# screenshot_process.py
import time
import os
from PIL import Image, ImageGrab

save_folder = "/Users/apple/Desktop/Python/Smarcle/PythonWeek/Notion/asset/screenshots"
os.makedirs(save_folder, exist_ok=True)

def take_screenshot(display, screenshot_queue):
    while True:
        bbox = (display['origin_x'], display['origin_y'], display['origin_x'] + display['width'], display['origin_y'] + display['height'])
        screenshot = ImageGrab.grab(bbox)
        screenshot = screenshot.resize((1920, 1080))  # 이미지 해상도를 1920x1080으로 규격화
        timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")
        screenshot_path = os.path.join(save_folder, f"screenshot_{timestamp}.png")
        screenshot.save(screenshot_path)
        screenshot_queue.put((screenshot_path, timestamp))
        time.sleep(1)  # *** 1초 대기합니다 ***
