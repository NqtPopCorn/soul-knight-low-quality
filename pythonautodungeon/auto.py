import pyautogui
import time

pyautogui.useImageNotFoundException()

def click_first_image(image_list, confidence_threshold=0.8):
    for image in image_list:
        try:
            location = pyautogui.locateOnScreen(image, confidence=confidence_threshold)
            if location:
                pyautogui.click(location)
                return True
        except pyautogui.ImageNotFoundException:
            pass
    return False

image_list = {'send.png', 'cuddle.png'}

while True:
    if click_first_image(image_list):
        time.sleep(2)  
    else:
        time.sleep(10)
        print("Không tìm thấy bất kỳ hình ảnh nào trong danh sách.")
    time.sleep(1)
