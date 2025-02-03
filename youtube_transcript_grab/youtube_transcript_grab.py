import pyautogui
import time

# Constants for delays (adjust as needed)
SHORT_DELAY = 2
LONG_DELAY = 5

# Function to find and click a button by its image
def click_button(image_path, confidence=0.8):
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            pyautogui.click(location)
            time.sleep(SHORT_DELAY)
            return True
        else:
            print(f"Button not found: {image_path}")
            return False
    except pyautogui.ImageNotFoundException:
        print(f"ImageNotFoundException for {image_path}")
        return False

# Function to scroll down until a button is found and clicked
def scroll_and_click(image_path, confidence=0.8, max_scrolls=10):
    for _ in range(max_scrolls):
        if click_button(image_path, confidence):
            return True
        pyautogui.scroll(-500)  # Scroll down
        time.sleep(SHORT_DELAY)
    print(f"Failed to find and click the button: {image_path}")
    return False

# Function to check if the end of the transcript is present
def check_transcript_end(transcript_end_img):
    try:
        end_location = pyautogui.locateCenterOnScreen(transcript_end_img, confidence=0.8)
        if not end_location:
            print("Transcript end image not found. Skipping to next video.")
            skip_to_next_video_and_pause()
            return False
        return True
    except pyautogui.ImageNotFoundException:
        print("ImageNotFoundException while checking for transcript end image. Skipping to next video.")
        skip_to_next_video_and_pause()
        return False
    except Exception as e:
        print(f"Unexpected error while checking for transcript end: {e}")
        skip_to_next_video_and_pause()
        return False

# Function to manually highlight and copy the transcript
def manual_highlight_and_copy(transcript_start_img, transcript_end_img):
    try:
        # Find the start of the transcript
        start_location = pyautogui.locateCenterOnScreen(transcript_start_img, confidence=0.8)
        if not start_location:
            print("Could not find the transcript start image.")
            return
        pyautogui.moveTo(start_location)
        pyautogui.move(-35, 50)  # Adjust slightly below the "Transcript" heading
        pyautogui.mouseDown()  # Hold mouse button

        # Find the end of the transcript
        end_location = pyautogui.locateCenterOnScreen(transcript_end_img, confidence=0.8)
        if not end_location:
            print("Could not find the transcript end image.")
            pyautogui.mouseUp()  # Release mouse in case of failure
            return
        pyautogui.moveTo(end_location, duration=1)  # Drag to the end of the transcript
        time.sleep(30)  # Allow time for full selection (adjust duration as needed)
        pyautogui.mouseUp()  # Release mouse button

        # Copy the highlighted text
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(SHORT_DELAY)
        print("Transcript copied.")
    except pyautogui.ImageNotFoundException as e:
        print(f"ImageNotFoundException during manual highlight: {e}")

# Function to copy the transcript to Notepad++
def copy_transcript():
    # Move to Notepad++ (adjust coordinates if needed)
    pyautogui.moveTo(1500, 200)  # Coordinates of Notepad++ area
    pyautogui.click()
    time.sleep(SHORT_DELAY)
    pyautogui.hotkey('ctrl', 'a')  # Select all text
    pyautogui.press('right')  # Move to the end of the document
    pyautogui.press('enter')  # Add a new line for the next transcript
    pyautogui.hotkey('ctrl', 'v')  # Paste text

# Function to skip to the next video and pause it
def skip_to_next_video_and_pause():
    # Move mouse over the video to ensure controls are visible
    pyautogui.moveTo(400, 400)  # Coordinates to hover over the video (adjust as needed)
    time.sleep(SHORT_DELAY)
    # Click the "Next" button using an image reference
    click_button('next_button.png')
    
    time.sleep(SHORT_DELAY)
    
    # Pause the video by clicking in the video area
    pyautogui.moveTo(300, 300)  # Move to video area
    pyautogui.click()  # Pause the video

# Main script
def main():
    num_videos = int(input("How many videos do you want to process? "))

    for _ in range(num_videos):
        # Expand video description
        click_button('show_more.png')

        # Open transcript (scroll down if necessary)
        if not scroll_and_click('show_transcript.png'):
            # Scroll back to the top by reversing the number of downward scrolls
            for _ in range(12):  # max_scrolls (10) + 2 extra scrolls
                pyautogui.scroll(500)
            time.sleep(SHORT_DELAY)

            # Skip to the next video and pause it
            skip_to_next_video_and_pause()
            continue  # Skip the rest of the loop for this iteration

        time.sleep(LONG_DELAY)

        # Check for transcript end image
        if not check_transcript_end('transcript_end.png'):
            continue

        # Highlight and copy transcript manually
        manual_highlight_and_copy('transcript_heading.png', 'transcript_end.png')

        # Paste into Notepad++
        copy_transcript()

        # Skip to the next video and pause it
        skip_to_next_video_and_pause()
        
        time.sleep(LONG_DELAY)

if __name__ == "__main__":
    print("Starting script in 5 seconds. Switch to YouTube.")
    time.sleep(5)  # Give the user time to switch to the YouTube window
    main()