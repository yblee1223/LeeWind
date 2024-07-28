# search_screen_main.py
import sys
sys.path.append('/Users/apple/Desktop/Python/Smarcle/PythonWeek/Notion/lib')

from search_process import search_keyword_in_ocr, load_ocr_results
from PIL import Image

def print_filtered_timestamps_with_screenshot(keyword, matching_timestamps, threshold):
    ocr_results = load_ocr_results()
    previous_count = None
    state = 0
    if matching_timestamps:
        print(f"키워드 '{keyword}'가 포함된 타임스탬프들 (필터링):")
        for timestamp in matching_timestamps:
            texts = ocr_results.get(timestamp, [])
            count = len(texts) if isinstance(texts, list) else len(texts.split('\n'))
            if previous_count is None or abs(count - previous_count) > threshold:
                state = 1
                print(f"{timestamp} : {count}")
                screenshot_path = f"/Users/apple/Desktop/Python/Smarcle/PythonWeek/Notion/asset/screenshots/screenshot_{timestamp}.png"
                try:
                    image = Image.open(screenshot_path)
                    image.show()
                except FileNotFoundError:
                    print(f"스크린샷 파일을 찾을 수 없습니다: {screenshot_path}")
            else:
                state = 0
            previous_count = count
    else:
        print(f"키워드 '{keyword}'를 포함하는 결과를 찾을 수 없습니다.")

def main():
    keyword = input("검색할 키워드를 입력해주세요: ").strip()
    threshold = 10  # 임계값 설정
    matching_timestamps = search_keyword_in_ocr(keyword)
    
    # 필터링된 타임스탬프와 해당 텍스트 개수 및 스크린샷 출력
    print_filtered_timestamps_with_screenshot(keyword, matching_timestamps, threshold)

if __name__ == "__main__":
    main()
