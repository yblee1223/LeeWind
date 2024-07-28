# main.py
import time
import threading
import queue
import sys

sys.path.append('/Users/apple/Desktop/Python/Smarcle/PythonWeek/Notion/lib')

from display_info import select_display
from screenshot_process import take_screenshot
from ocr_process import extract_text_from_image
from analyze import analyze_screenshot

def main():
    display = select_display()
    screenshot_queue = queue.Queue()
    processed_queue = queue.Queue()
    screenshot_list = []

    # 5초 대기 후 스크린샷 촬영 시작
    for i in range(5, 0, -1):
        sys.stdout.write(f"\rStarting in {i} seconds...")
        sys.stdout.flush()
        time.sleep(1)
    print("\nStarting screenshot capture...")

    # 스크린샷을 찍는 쓰레드 시작
    screenshot_thread = threading.Thread(target=take_screenshot, args=(display, screenshot_queue))
    screenshot_thread.daemon = True
    screenshot_thread.start()

    # OCR 및 텍스트 처리를 하는 쓰레드 시작
    ocr_thread = threading.Thread(target=extract_text_from_image, args=(screenshot_queue, processed_queue))
    ocr_thread.daemon = True
    ocr_thread.start()

    print("되돌아 갈 시간을 입력해주세요: ", end="")

    while True:
        try:
            N = int(input())
            while not processed_queue.empty():
                screenshot_list.append(processed_queue.get())
            analyze_screenshot(screenshot_list, N)
            answer = input("다시 실행하시겠습니까? (yes 또는 y 입력시 재실행): ").strip().lower()
            if answer not in ("yes", "y"):
                print("Exiting program.")
                break
            else:
                print("되돌아 갈 시간을 입력해주세요: ", end="")
        except ValueError:
            print("Please enter a valid integer.")
            print("되돌아 갈 시간을 입력해주세요: ", end="")
        except KeyboardInterrupt:
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()
