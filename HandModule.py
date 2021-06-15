import cv2
import time
import mediapipe as mp
import random


class handDetection():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        
        # Initialization
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,
                                self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    # Function to find hands on img    
    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # when no hand in image we get None
        if self.results.multi_hand_landmarks:
            for self.handLms in self.results.multi_hand_landmarks:
                if draw: 
                    # If draw == True, draw landmarks on image
                    self.mpDraw.draw_landmarks(img, self.handLms, self.mpHands.HAND_CONNECTIONS)
        return img    

    def pointPositions(self, img):
        self.positions = []
        if self.results.multi_hand_landmarks:

            for id, lm in enumerate(self.handLms.landmark):
                #print(id,lm)

                # This gives us coordinates of hand-points
                w, h, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.positions.append((cx,cy))  
        return self.positions 

    def rockpaperscissors(self, img):
        # https://google.github.io/mediapipe/solutions/hands.html shows indexing of fingers
        open_fingers=[]
        # We will look at extreme points of 4 fingers, ignore the thumb
        finger_points=[8,12,16,20]
        # Set hand to none
        hand = "None"
        #Hand has 21 points, 1 for wrist, 20 for fingers
        if (len(self.positions) == 21):
            for i in finger_points:
                
                #print(self.positions[i])
                # If top point of finger has lower y-coordinate than the points 2 positions lower, the finger is open
                # in cv2 top left corner of image is (0,0). This means points with lower y-coordinates are higher. 
                if self.positions[i][1] < self.positions[i-2][1]:
                    open_fingers.append(1)
                else:
                    open_fingers.append(0)

            # combinations of open fingers for rock, paper or scissors  
            # This is a very primitive classification.   
            if open_fingers == [1,1,1,1]:
                hand = "PAPER"    
            elif open_fingers == [1,1,0,0]:
                hand = "SCISSORS"
            elif open_fingers == [0,0,0,0]:  
                hand = "ROCK" 

        return hand

    def play_a_game(self):
        # Function returns rock, paper or scissors
        moves = ["ROCK","PAPER","SCISSORS"]
        return moves[random.randint(0,2)]


def main():
    # Start webcam
    cap = cv2.VideoCapture(0)
    imageDetector = handDetection()

    print(random.randint(0,3))

     # Time from start
    time_start=time.time()

    # Show until False
    ok_flag = True 
    count = 0
    while ok_flag:
        (ok_flag, img) = cap.read()
        img = imageDetector.findHands(img) 
        lst =  imageDetector.pointPositions(img)
        rps = imageDetector.rockpaperscissors(img)
        
        # Time since starting the program (current time)
        cTime = time.time() - time_start

        # Show time 
        cv2.putText(img, str(int(cTime)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        # Show if R P OR S
        cv2.putText(img, rps, (10,450), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        if cTime < 5:
            cv2.putText(img, "Pick", (400,450), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 1)
  
        else:
            
            if (count == 0):
                count = 1
                play = imageDetector.play_a_game()
            print(count)    

            cv2.putText(img, play, (400,40), cv2.FONT_HERSHEY_PLAIN, 3, (255,200,255), 3)
        
            if play == rps:
                cv2.putText(img, "DRAW", (10,40), cv2.FONT_HERSHEY_PLAIN, 3, (255,200,255), 3)
            elif((play == "ROCK") & (rps == "PAPER") ) :
                cv2.putText(img, "WON", (10,40), cv2.FONT_HERSHEY_PLAIN, 3, (255,200,255), 3)
            elif((play == "ROCK") & (rps == ("SCISSORS")) ) :
                cv2.putText(img, "LOST", (10,40), cv2.FONT_HERSHEY_PLAIN, 3, (255,200,255), 3)        
            elif((play == "PAPER") & (rps == "SCISSORS") ) :
                cv2.putText(img, "WON", (10,40), cv2.FONT_HERSHEY_PLAIN, 3, (255,200,255), 3)          
            elif((play == "PAPER") & (rps == "ROCK") ) :
                cv2.putText(img, "WON", (10,40), cv2.FONT_HERSHEY_PLAIN, 3, (255,200,255), 3) 
            elif((play == "SCISSORS") & (rps == "ROCK") ) :
                cv2.putText(img, "WON", (10,40), cv2.FONT_HERSHEY_PLAIN, 3, (255,200,255), 3)        
            elif((play == "SCISSORS") & (rps == "PAPER") ) :
                cv2.putText(img, "LOST", (10,40), cv2.FONT_HERSHEY_PLAIN, 3, (255,200,255), 3)

            if cTime >= 10:
                time_start = cTime;
                count = 0
                break;

        # Show frame
        cv2.imshow("CallingCamera View", img)
        
        # Close the window by pressing ESC
        if cv2.waitKey(1) == 27:
            ok_flag = False

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main() 