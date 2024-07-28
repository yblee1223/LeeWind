import sys
import os
import json
from PIL import Image, ImageDraw, ImageFont
sys.path.append('/Users/apple/Desktop/Python/Smarcle/PythonWeek/Notion/lib')

from search_process import search_keyword_in_ocr, load_ocr_results

def highlight_text_in_image(image_path, keyword, ocr_data, highlight_color=(255, 165, 0, 128)):
    try:
        image = Image.open(image_path).convert("RGBA")
        overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        font = ImageFont.load_default()

        for item in ocr_data["value"]:
            text = item["text"]
            if keyword in text:
                bbox = item["bbox"]
                bbox = [(bbox[0][0], bbox[0][1]), (bbox[2][0], bbox[2][1])]
                # 채워진 사각형을 그려 하이라이트 색상을 적용합니다.
                draw.rectangle(bbox, fill=highlight_color)
                # 텍스트를 빨간색으로 표시합니다.
                # draw.text((bbox[0][0], bbox[0][1]), text, fill="red", font=font)

        combined = Image.alpha_composite(image, overlay)
        combined.show()
    except FileNotFoundError:
        print(f"스크린샷 파일을 찾을 수 없습니다: {image_path}")

def print_filtered_timestamps_with_screenshot_and_highlight(keyword, matching_timestamps, threshold):
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
                json_path = f"/Users/apple/Desktop/Python/Smarcle/PythonWeek/Notion/asset/json/{timestamp}.json"
                try:
                    with open(json_path, "r", encoding="utf-8") as json_file:
                        ocr_data = json.load(json_file)
                    highlight_text_in_image(screenshot_path, keyword, ocr_data)
                except FileNotFoundError:
                    print(f"JSON 파일을 찾을 수 없습니다: {json_path}")
            else:
                state = 0
            previous_count = count
    else:
        print(f"키워드 '{keyword}'를 포함하는 결과를 찾을 수 없습니다.")

def main():
    keyword = input("검색할 키워드를 입력해주세요: ").strip()
    threshold = 10  # 임계값 설정
    matching_timestamps = search_keyword_in_ocr(keyword)
    
    # 필터링된 타임스탬프와 해당 텍스트 개수 및 스크린샷 출력 및 하이라이트
    print_filtered_timestamps_with_screenshot_and_highlight(keyword, matching_timestamps, threshold)

if __name__ == "__main__":
    main()