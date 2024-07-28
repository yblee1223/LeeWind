# search_main.py
from search_process import search_keyword_in_ocr, load_ocr_results

def print_timestamps_only(keyword, matching_timestamps):
    if matching_timestamps:
        print(f"키워드 '{keyword}'가 포함된 타임스탬프들:")
        for timestamp in matching_timestamps:
            print(timestamp)
    else:
        print(f"키워드 '{keyword}'를 포함하는 결과를 찾을 수 없습니다.")

def print_timestamps_with_count(keyword, matching_timestamps):
    ocr_results = load_ocr_results()
    if matching_timestamps:
        print(f"'{keyword}' 키워드가 포함된 타임스탬프 검색 결과:")
        for timestamp in matching_timestamps:
            texts = ocr_results.get(timestamp, [])
            count = len(texts) if isinstance(texts, list) else len(texts.split('\n'))
            print(f"{timestamp} : {count}")
    else:
        print(f"키워드 '{keyword}'를 포함하는 결과를 찾을 수 없습니다.")

def main():
    keyword = input("검색할 키워드를 입력해주세요: ").strip()
    matching_timestamps = search_keyword_in_ocr(keyword)
    
    # 키워드가 포함된 타임스탬프 출력
    # print_timestamps_only(keyword, matching_timestamps)
    
    # 키워드가 포함된 타임스탬프와 해당 텍스트 개수 출력
    print_timestamps_with_count(keyword, matching_timestamps)

if __name__ == "__main__":
    main()
