import AppKit
import subprocess
import time

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

def get_active_window_info():
    apple_script = '''
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        set frontAppName to name of frontApp
        set windowTitle to ""
        try
            tell process frontAppName
                set windowTitle to name of first window
            end tell
        end try
        return {frontAppName, windowTitle}
    end tell
    '''
    
    result = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True)
    if result.stderr:
        return None
    result = result.stdout.strip().split(",")[0]
    return result

if __name__ == "__main__":
    time.sleep(5)
    window_title = get_active_window_info()
    print(window_title)