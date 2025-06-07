# Import necessary libraries
import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7, max_num_hands=2)
mpDraw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

# Variable to avoid continuous scrolling
scrolling_left = False
scrolling_right = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_idx, handLms in enumerate(results.multi_hand_landmarks):
            lmList = []

            # Get hand label (Left or Right)
            hand_label = results.multi_handedness[hand_idx].classification[0].label

            # Get coordinates of landmarks
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))

            if lmList:
                index_tip_y = lmList[8][2]
                thumb_tip_y = lmList[4][2]

                # If difference in y-coordinates is big enough, trigger scroll
                if abs(index_tip_y - thumb_tip_y) > 50:
                    if hand_label == "Left" and not scrolling_left:
                        pyautogui.scroll(80)  # Scroll UP
                        scrolling_left = True
                        print("Scroll Up with Left Hand")
                    elif hand_label == "Right" and not scrolling_right:
                        pyautogui.scroll(-80)  # Scroll DOWN
                        scrolling_right = True
                        print("Scroll Down with Right Hand")
                else:
                    # Reset scrolling flags when gesture ends
                    if hand_label == "Left":
                        scrolling_left = False
                    elif hand_label == "Right":
                        scrolling_right = False

            # Draw hand landmarks
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # Show the camera feed
    cv2.imshow("Hand Gesture", img)

    # Press Esc key to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
