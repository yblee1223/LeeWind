import subprocess

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
    window_title = get_active_window_info()
    print(window_title)