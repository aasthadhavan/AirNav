"""AirNav - Virtual Mouse Navigator

This project allows control of the computer cursor using hand gestures via webcam.
Features:
    - Cursor movement (index finger)
    - Left click (index + middle pinch)
    - Right click (3 fingers up)
    - Smooth scrolling (2 fingers up, vertical motion)
    - Volume control (thumb ↔ index distance)
Libraries: OpenCV, CVZone (Mediapipe Hands), PyAutoGUI, Pycaw
"""

"""importing libraries"""
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import numpy as np
import time
"""for volume control"""
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

"""setting up the webcam"""
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

"""hand detector"""
detector = HandDetector(detectionCon=0.8, maxHands=1)

"screen size"""
screen_w, screen_h = pyautogui.size()

"""movement smoothening"""
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0

"""click cooldown"""
last_click_time = 0
click_delay = 0.3  # in seconds

"""volume setup"""
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()  # (-65.25, 0.0, 0.03125)
min_vol, max_vol = vol_range[0], vol_range[1]

"""scroll memory"""
prev_scroll_y = None

"""volume smoothening"""
prev_vol_level = None

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # mirrored 
    gesture_label = ""  # text label for gesture

    hands, img = detector.findHands(img)

    if hands:
        lmList = hands[0]["lmList"]
        fingers = detector.fingersUp(hands[0])

        if lmList:
            x, y = lmList[8][0:2]  # index fingertip

            #cursor movement
            screen_x = np.interp(x, [100, 1180], [0, screen_w])
            screen_y = np.interp(y, [100, 620], [0, screen_h])
            clocX = plocX + (screen_x - plocX) / smoothening
            clocY = plocY + (screen_y - plocY) / smoothening
            pyautogui.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY

            #pinch distance for left click 
            pinch_dist = detector.findDistance(lmList[8][0:2], lmList[12][0:2])[0]

            #left click
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and pinch_dist < 40:
                current_time = time.time()
                if current_time - last_click_time > click_delay:
                    pyautogui.click()
                    last_click_time = current_time
                    cv2.circle(img, (int(clocX), int(clocY)), 15, (0, 255, 0), cv2.FILLED)
                    gesture_label = "Left Click"

            #right Click (3 fingers up)
            elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                current_time = time.time()
                if current_time - last_click_time > click_delay:
                    pyautogui.rightClick()
                    last_click_time = current_time
                    cv2.circle(img, (int(clocX), int(clocY)), 15, (0, 0, 255), cv2.FILLED)
                    gesture_label = "Right Click"

            #smooth scroll (2 fingers up) 
            elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                if prev_scroll_y is None:
                    prev_scroll_y = y
                dy = y - prev_scroll_y
                smooth_dy = dy / 2  
                if abs(smooth_dy) > 5:
                    pyautogui.scroll(-int(smooth_dy * 3))
                prev_scroll_y += smooth_dy
                cv2.circle(img, (int(clocX), int(clocY)), 15, (0, 255, 255), cv2.FILLED)  
                gesture_label = "Scrolling"
            else:
                prev_scroll_y = None

            #volume control (thumb ↔ index) 
            dist_vol, _, _ = detector.findDistance(lmList[4][0:2], lmList[8][0:2])
            dist_vol = max(dist_vol, 20)  
            vol_level = np.interp(dist_vol, [20, 200], [min_vol, max_vol])
            if prev_vol_level is None:
                prev_vol_level = vol_level
            vol_level = prev_vol_level + (vol_level - prev_vol_level) / 5
            prev_vol_level = vol_level
            volume.SetMasterVolumeLevel(vol_level, None)

            if fingers[0] == 1 and fingers[1] == 1 and abs(dist_vol - prev_vol_level) > 1:
                cv2.circle(img, (lmList[4][0], lmList[4][1]), 15, (255, 0, 0), cv2.FILLED)
                gesture_label = "Volume"

            #displaying gesture label 
            if gesture_label != "":
                cv2.putText(img, gesture_label, (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 255, 255), 3)

    #displaying webcam feed
    cv2.imshow("AirNav - Virtual Mouse", img)

    #quit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
