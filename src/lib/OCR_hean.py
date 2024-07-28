import time  # 시간 관련 기능을 위한 모듈
import os  # 운영체제 관련 기능을 위한 모듈
import easyocr  # OCR(Optical Character Recognition) 기능을 위한 모듈
import cv2  # 컴퓨터 비전 기능을 위한 OpenCV 모듈
from PIL import Image, ImageGrab  # 이미지 처리 및 스크린샷 캡처를 위한 PIL 모듈
import AppKit  # macOS에서 화면 관련 기능을 위한 모듈
import threading  # 멀티스레딩 기능을 위한 모듈
import queue  # 스레드 간의 통신을 위한 큐 모듈
import subprocess  # 외부 명령 실행을 위한 모듈
import sys  # 시스템 관련 기능을 위한 모듈
import json  # JSON 처리 기능을 위한 모듈
from deep_translator import GoogleTranslator  # 번역 기능을 위한 모듈
import numpy as np  # 수치 계산을 위한 NumPy 모듈
import sys
import pyautogui

# sys.path.append(os.getcwd())

def set_enviroment():
    start = time.time()  # 시작 시간 기록
    ocr_model = easyocr.Reader(['ko', 'en'], gpu=True)  # EasyOCR 모델 로딩 (한국어와 영어 지원)
    print(f"Model loading time: {time.time() - start}")  # 모델 로딩 시간 출력

    save_folder = "data/screenshots"
    os.makedirs(save_folder, exist_ok=True)  
    text_save_folder = "data/texts"
    os.makedirs(text_save_folder, exist_ok=True)  
    ocr_json_folder = "data/jsons"
    os.makedirs(ocr_json_folder, exist_ok=True) 

def get_display_info():
    """
    시스템의 디스플레이 정보를 가져옵니다.
    """
    screens = AppKit.NSScreen.screens()  # 모든 디스플레이 화면 정보를 가져옴
    display_info = []  # 디스플레이 정보를 저장할 리스트
    for i, screen in enumerate(screens):
        frame = screen.frame()  # 각 디스플레이의 프레임 정보 가져오기
        display_info.append({
            "id": i,  # 디스플레이 ID
            "width": int(frame.size.width),  # 디스플레이 너비
            "height": int(frame.size.height),  # 디스플레이 높이
            "origin_x": int(frame.origin.x),  # 디스플레이 시작 x 좌표
            "origin_y": int(frame.origin.y)  # 디스플레이 시작 y 좌표
        })
    return display_info  # 디스플레이 정보 리스트 반환

def select_display():
    """
    사용자가 캡처할 디스플레이를 선택하도록 합니다.
    """
    display_info = get_display_info()  # 디스플레이 정보 가져오기
    for display in display_info:
        # 각 디스플레이 정보 출력
        print(f"ID: {display['id']}, Width: {display['width']}, Height: {display['height']}, X: {display['origin_x']}, Y: {display['origin_y']}")
    selected_id = int(input("Select the display ID to capture: "))  # 사용자로부터 선택된 디스플레이 ID 입력받기
    return display_info[selected_id]  # 선택된 디스플레이 정보 반환

def take_screenshot(display, screenshot_queue):
    """
    선택된 디스플레이의 스크린샷을 주기적으로 캡처하여 큐에 저장합니다.
    """
    while True:
        bbox = (display['origin_x'], display['origin_y'], display['origin_x'] + display['width'], display['origin_y'] + display['height'])  # 캡처할 영역 설정
        screenshot = ImageGrab.grab(bbox)  # 스크린샷 캡처
        screenshot = screenshot.resize((1920, 1080))  # 이미지 해상도를 1920x1080으로 규격화
        timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")  # 타임스탬프 생성
        screenshot_path = os.path.join(save_folder, f"screenshot_{timestamp}.png")  # 스크린샷 파일 경로 생성
        screenshot.save(screenshot_path)  # 스크린샷 저장
        screenshot_queue.put((screenshot_path, timestamp))  # 스크린샷 경로와 타임스탬프를 큐에 저장
        time.sleep(1)  # 1초 대기

def convert_to_serializable(result):
    """
    OCR 결과를 JSON 직렬화 가능한 형식으로 변환합니다.
    """
    serializable_result = []  # 직렬화 가능한 결과를 저장할 리스트
    for item in result:
        serializable_item = {
            "bbox": [list(map(float, point)) for point in item[0]],  # numpy 배열을 float 리스트로 변환
            "text": item[1],  # 텍스트
            "prob": float(item[2])  # 확률
        }
        serializable_result.append(serializable_item)  # 리스트에 추가
    return serializable_result  # 직렬화 가능한 결과 리스트 반환

def extract_text_from_image(screenshot_queue, processed_queue):
    """
    큐에서 스크린샷을 가져와 OCR을 수행하고 결과를 처리합니다.
    """
    while True:
        screenshot_path, timestamp = screenshot_queue.get()  # 큐에서 스크린샷 경로와 타임스탬프 가져오기
        image = cv2.imread(screenshot_path)  # 스크린샷 이미지 읽기
        image = cv2.resize(image, (1920, 1080))  # 이미지 해상도를 1920x1080으로 규격화
        result = ocr_model.readtext(image, batch_size=16)  # OCR 수행 (Batch size를 16으로 설정하여 속도 향상)
        result = convert_to_serializable(result)  # 결과를 직렬화 가능한 형식으로 변환

        # JSON 파일 저장
        time_value = timestamp[2:4] + timestamp[5:7] + timestamp[8:10] + timestamp[11:13] + timestamp[14:16] + timestamp[17:19]  # 시간 값 생성
        ocr_result = {
            "time": time_value,  # 시간 값
            "value": result  # OCR 결과
        }
        ocr_json_path = os.path.join(ocr_json_folder, f"ocr_{timestamp}.json")  # JSON 파일 경로 생성
        with open(ocr_json_path, "w", encoding="utf-8") as json_file:
            json.dump(ocr_result, json_file, ensure_ascii=False, indent=4)  # JSON 파일로 저장

        text = "\n".join([detection["text"] for detection in result])  # OCR 결과에서 텍스트 추출
        processed_queue.put((screenshot_path, text, timestamp))  # 처리된 결과를 큐에 저장
        screenshot_queue.task_done()  # 큐 작업 완료

        # 추출한 텍스트 저장
        with open(os.path.join(text_save_folder, f"text_{timestamp}.txt"), "w", encoding="utf-8") as f:
            f.write(f"[OCR 결과]\n'{text}'")  # 텍스트 파일로 저장

def summarize_with_llama(text):
    """
    Llama 모델을 사용하여 텍스트를 요약합니다.
    """
    command = f"ollama run llama3 \"Summarize this: {text}\""  # 요약 명령 생성
    result = subprocess.run(command, shell=True, capture_output=True, text=True)  # 명령 실행
    summary_en = result.stdout.strip()  # 요약 결과 추출
    summary_ko = GoogleTranslator(source='en', target='ko').translate(summary_en)  # 요약 결과를 한국어로 번역
    return summary_ko  # 번역된 요약 결과 반환

def analyze_screenshot(screenshot_list, N):
    """
    주어진 시간 N 초 이전의 스크린샷을 분석하고 텍스트를 출력합니다.
    """
    current_time = time.time()  # 현재 시간
    target_time = current_time - N  # 목표 시간 (N 초 이전)

    for screenshot_path, text, timestamp in reversed(screenshot_list):
        screenshot_time = time.mktime(time.strptime(timestamp, "%Y_%m_%d_%H_%M_%S"))  # 스크린샷의 시간
        if screenshot_time <= target_time:
            image = Image.open(screenshot_path)  # 스크린샷 이미지 열기
            image.show()  # 스크린샷을 화면에 표시

            text_file_path = os.path.join(text_save_folder, f"text_{timestamp}.txt")  # 텍스트 파일 경로 생성
            with open(text_file_path, "r", encoding="utf-8") as f:
                text_content = f.read()  # 텍스트 파일 읽기

            # print(f"{text_content}")  # OCR 결과 주석 처리

            # 비동기적으로 요약 작업을 수행
            summary_thread = threading.Thread(target=summarize_and_print, args=(text_content,))
            summary_thread.start()
            summary_thread.join()  # 요약이 완료될 때까지 대기

            return  # 분석 완료 후 함수 종료

    print(f"No screenshot found for {N} seconds ago.")  # 해당 시간 이전의 스크린샷이 없는 경우 메시지 출력

def summarize_and_print(text_content):
    """
    주어진 텍스트를 요약하고 출력합니다.
    """
    summary = summarize_with_llama(text_content)  # 텍스트 요약
    print(f"[상황 요약]\n'{summary}'")  # 요약 결과 출력

def main():
    """
    프로그램의 메인 함수입니다.
    """
    display = select_display()  # 디스플레이 선택
    screenshot_queue = queue.Queue()  # 스크린샷 큐 생성
    processed_queue = queue.Queue()  # 처리된 결과 큐 생성
    screenshot_list = []  # 스크린샷 리스트

    # 5초 대기 후 스크린샷 촬영 시작
    for i in range(5, 0, -1):
        sys.stdout.write(f"\rStarting in {i} seconds...")  # 시작 시간 카운트다운 출력
        sys.stdout.flush()
        time.sleep(1)  # 1초 대기
    print("\nStarting screenshot capture...")  # 스크린샷 촬영 시작 메시지 출력

    # 스크린샷을 찍는 쓰레드 시작
    screenshot_thread = threading.Thread(target=take_screenshot, args=(display, screenshot_queue))
    screenshot_thread.daemon = True  # 메인 스레드가 종료될 때 같이 종료
    screenshot_thread.start()  # 스레드 시작

    # OCR 및 텍스트 처리를 하는 쓰레드 시작
    ocr_thread = threading.Thread(target=extract_text_from_image, args=(screenshot_queue, processed_queue))
    ocr_thread.daemon = True  # 메인 스레드가 종료될 때 같이 종료
    ocr_thread.start()  # 스레드 시작

    print("되돌아 갈 시간을 입력해주세요: ", end="")  # 사용자 입력 요청

    while True:
        try:
            N = int(input())  # 사용자 입력 받기
            while not processed_queue.empty():
                screenshot_list.append(processed_queue.get())  # 처리된 결과를 스크린샷 리스트에 추가
            analyze_screenshot(screenshot_list, N)  # 스크린샷 분석
            answer = input("다시 실행하시겠습니까? (yes 또는 y 입력시 재실행): ").strip().lower()  # 재실행 여부 묻기
            if answer not in ("yes", "y"):
                print("Exiting program.")  # 프로그램 종료 메시지 출력
                break  # 반복문 종료
            else:
                print("되돌아 갈 시간을 입력해주세요: ", end="")  # 사용자 입력 요청
        except ValueError:
            print("Please enter a valid integer.")  # 유효한 정수를 입력하지 않은 경우 메시지 출력
            print("되돌아 갈 시간을 입력해주세요: ", end="")  # 사용자 입력 요청
        except KeyboardInterrupt:
            print("Exiting program.")  # 프로그램 종료 메시지 출력
            break  # 반복문 종료

if __name__ == "__main__":
    set_enviroment()
    main()  # 메인 함수 실행
