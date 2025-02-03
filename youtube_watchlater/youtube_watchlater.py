import pyautogui
import time

# Constants - Adjust these as needed
VIDEO_OFFSET_X = 120  # Horizontal distance to move to the next video
VIDEO_OFFSET_Y = 250  # Vertical distance to move down a row
SCROLL_PIXELS = -150  # Negative value scrolls down; adjust based on your setup
SCROLL_WAIT_TIME = 3  # Time to wait after scrolling
WATCH_LATER_ICON = "watch_later_icon.png"  # Path to the Watch Later button image

# Global Variables
initial_x = None
initial_y = None
current_row_y = None  # To track the Y position of the current row

def wait_and_position_cursor():
    """
    Pauses for 5 seconds, records the initial cursor position.
    """
    global initial_x, initial_y, current_row_y
    print("Place your cursor on the first video thumbnail. Script starting in 5 seconds...")
    time.sleep(5)
    initial_x, initial_y = pyautogui.position()
    current_row_y = initial_y
    print(f"Initial cursor position recorded at: ({initial_x}, {initial_y})")

def reset_cursor_to_first_row():
    """
    Resets the cursor to the first visible row after scrolling.
    """
    global current_row_y
    current_row_y = initial_y  # Reset row to the first visible row
    pyautogui.moveTo(initial_x, current_row_y, duration=0.5)
    print(f"Cursor reset to first row: ({initial_x}, {current_row_y})")

def locate_and_click_watch_later():
    """
    Locates the Watch Later button on the screen and clicks it.
    Returns True if the button is found and clicked, else False.
    """
    try:
        watch_later_pos = pyautogui.locateCenterOnScreen(WATCH_LATER_ICON, confidence=0.8)
        if watch_later_pos:
            pyautogui.moveTo(watch_later_pos)
            pyautogui.click()
            time.sleep(0.5)  # Small delay for stability
            return True
    except Exception as e:
        print(f"Error locating Watch Later button: {e}")
    return False

def move_to_next_video():
    """
    Moves the cursor horizontally to the next video.
    """
    pyautogui.moveRel(VIDEO_OFFSET_X, 0, duration=0.2)

def move_to_next_row():
    """
    Moves the cursor back to the first video position and down to the next row.
    """
    global current_row_y
    current_row_y += VIDEO_OFFSET_Y
    pyautogui.moveTo(initial_x, current_row_y, duration=0.5)
    print(f"Moved to the next row at Y: {current_row_y}")

def scroll_down_and_wait():
    """
    Scrolls down the page, resets the cursor to the first visible row.
    """
    pyautogui.scroll(SCROLL_PIXELS)
    print("Scrolled down, waiting for videos to load...")
    time.sleep(SCROLL_WAIT_TIME)
    reset_cursor_to_first_row()

def process_videos():
    """
    Main function to process all videos on the page.
    """
    while True:
        for row in range(100):  # Arbitrary high number to keep processing rows
            for video in range(4):  # 4 videos per row
                success = locate_and_click_watch_later()
                if not success:
                    print("Watch Later button not found. Scrolling down...")
                    scroll_down_and_wait()
                    break  # Break inner loop to scroll down and reset
                move_to_next_video()
            else:
                move_to_next_row()
                continue
            break  # Break outer loop to restart after scrolling down

if __name__ == "__main__":
    try:
        wait_and_position_cursor()
        process_videos()
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
