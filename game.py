import cv2
import mediapipe as mp
import numpy as np
import random
#this game works by pointing in half of the screen if you point in one half it moves in that half and hit box is not the entire player but just the player position I wasn't able to improve that
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

score = 0
width, height = 1280, 640
player_pos = [320, 440]
x=random.randint(300,1200)
y=90

def enemy():
    global y  , x ,score
    cv2.circle(frame, (x, y), 100, (255, 0, 0), cv2.FILLED)
    y+=5
def enemy_move():
    global y  , x ,score
    if y == 650:
        score+=1
        print("passed")
        y=90
        x=random.randint(player_pos[0]-100,player_pos[0]+100)

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
def player():
    head_radius = 25
    body_length = 100
    black=(0,0,0)
    # Draw the head (circle)
    cv2.circle(frame, (player_pos[0], player_pos[1] - 30), head_radius, black, -1)

    # Draw the body (line)
    cv2.line(frame, (player_pos[0], player_pos[1]), (player_pos[0], player_pos[1] + body_length), black, 3) 
    # Draw the left arm (line)
    cv2.line(frame, (player_pos[0], player_pos[1] + 30), (player_pos[0] - 50, player_pos[1] + 50), black, 3) 
    # Draw the right arm (line)
    cv2.line(frame, (player_pos[0], player_pos[1] + 30), (player_pos[0] + 50, player_pos[1] + 50), black, 3)  

    # Draw the left leg (line)
    cv2.line(frame, (player_pos[0], player_pos[1] + body_length), (player_pos[0] - 30, player_pos[1] + body_length + 70), black, 3)  

    # Draw the right leg (line)
    cv2.line(frame, (player_pos[0], player_pos[1] + body_length), (player_pos[0] + 30, player_pos[1] + body_length + 70), black, 3)  

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue


    frame = cv2.resize(frame, (width, height))


    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)


    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 0, 255)
    
    enemy()
    enemy_move()
    player()
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            landmark_8 = hand_landmarks.landmark[8]


            h, w, _ = frame.shape
            cx, cy = int(landmark_8.x * w), int(landmark_8.y * h)
            cv2.circle(frame, (cx, cy), 20, (255, 0, 0), cv2.FILLED)
            try:
                if cx>640 and player_pos[0] in range(0,1280):
                    player_pos[0]+=10
                elif cx<640 and player_pos[0] in range(0,1280):
                    player_pos[0]-=10
                elif player_pos[0]>=1280:
                    player_pos[0]-=10
                elif player_pos[0]<=1280:
                    player_pos[0]+=10

                if player_pos[0] in range(x-120,x+120):
                    if player_pos[1] in range(y-120,y+120):
                        score="game over"
                        x=1400
                        print("found")
                       
            except Exception as e:
                print(e)


    m_frame = cv2.flip(frame, 1)
    tex1=cv2.putText(m_frame,"Score",(30,30),font,1,color,4,cv2.LINE_AA)
    text=cv2.putText(m_frame,str(score),(30,65),font,1,color,4,cv2.LINE_AA)
    cv2.imshow('Object Dodging Game', m_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
