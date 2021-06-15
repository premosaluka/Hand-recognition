import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(0)
ok_flag = True 

mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils

time_start = time.time()


while ok_flag:

    (ok_flag, img) = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # when no hand in image we get None
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                print(id,lm)

                # This gives us coordinates of hand-points
                w, h, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)    

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    cTime = time.time() - time_start
    cv2.putText(img, str(int(cTime)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("CallingCamera View", img)
    
    # Close the window by pressing ESC
    if cv2.waitKey(1) == 27:
        ok_flag = False

cv2.destroyAllWindows()