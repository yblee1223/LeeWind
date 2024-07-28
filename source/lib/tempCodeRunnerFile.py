# search_main.py
from search_process import search_keyword_in_ocr

def main():
    keyword = input("검색할 키워드를 입력해주세요: ").strip()
    matching_timestamps = search_keyword_in_ocr(keyword)
    
    if matching_timestamps:
        print(f"키워드 '{keyword}'가 포함된 타임스탬프들:")
        for timestamp in matching_timestamps:
            print(timestamp)
    else:
        print(f"키워드 '{keyword}'를 포함하는 결과를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
