import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(0)
ok_flag = True 

mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils

while ok_flag:

    (ok_flag, img) = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    print(results.multi_hand_landmarks)

    # when no hand in image we get None
    if results.multi_hand_landmarks:
    	for handLms in results.multi_hand_landmarks:
    		mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)



    cv2.imshow("CallingCamera View", img)
    
    cTime = time.time()
    #cv2.putText(img,str(int(cTime)),(10,50),c)

    # Close the window by pressing ESC
    if cv2.waitKey(1) == 27:
        ok_flag = False

cv2.destroyAllWindows()