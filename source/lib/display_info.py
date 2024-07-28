# display_info.py
import AppKit

def get_display_info():
    screens = AppKit.NSScreen.screens()
    display_info = []
    for i, screen in enumerate(screens):
        frame = screen.frame()
        display_info.append({
            "id": i,
            "width": int(frame.size.width),
            "height": int(frame.size.height),
            "origin_x": int(frame.origin.x),
            "origin_y": int(frame.origin.y)
        })
    return display_info

def select_display():
    display_info = get_display_info()
    for display in display_info:
        print(f"ID: {display['id']}, Width: {display['width']}, Height: {display['height']}, X: {display['origin_x']}, Y: {display['origin_y']}")
    selected_id = int(input("Select the display ID to capture: "))
    return display_info[selected_id]
