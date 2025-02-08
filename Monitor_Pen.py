import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

genislik, yukseklik = 100, 50
kalem_button = (20, 20, genislik, yukseklik)
silgi_button = (150, 20, genislik, yukseklik)

canvas = np.zeros((480, 640, 3), dtype=np.uint8)
cap = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    mode = 'kalem'
    drawing = False
    last_finger_position = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        sonuc = hands.process(rgb_frame)
        cv2.rectangle(frame, kalem_button[:2], (kalem_button[0] + genislik, kalem_button[1] + yukseklik), (255, 0, 0), -1)
        cv2.putText(frame, "Kalem", (kalem_button[0] + 10, kalem_button[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.rectangle(frame, silgi_button[:2], (silgi_button[0] + genislik, silgi_button[1] + yukseklik), (0, 255, 0), -1)
        cv2.putText(frame, "Silgi", (silgi_button[0] + 10, silgi_button[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if sonuc.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(sonuc.multi_hand_landmarks):
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                height, width, _ = frame.shape
                index_tip = hand_landmarks.landmark[8]
                finger_x, finger_y = int(index_tip.x * width), int(index_tip.y * height)
                thumb_tip = hand_landmarks.landmark[4]

                if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
                    index_up = True
                else:
                    index_up = False

                handedness = "Right"
                if sonuc.multi_handedness:
                    handedness = sonuc.multi_handedness[idx].classification[0].label

                if handedness == "Right":
                    thumb_up = True if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else False
                else:
                    thumb_up = True if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x else False

                if (kalem_button[0] < finger_x < kalem_button[0] + genislik and kalem_button[1] < finger_y < kalem_button[1] + yukseklik):
                    mode = 'kalem'
                    last_finger_position = None
                elif (silgi_button[0] < finger_x < silgi_button[0] + genislik and silgi_button[1] < finger_y < silgi_button[1] + yukseklik):
                    mode = 'silgi'
                    last_finger_position = None

                if mode == 'kalem':
                    if index_up and not thumb_up:
                        drawing = True
                        if last_finger_position is not None:
                            cv2.line(canvas, last_finger_position, (finger_x, finger_y), (255, 0, 0), 5)
                        last_finger_position = (finger_x, finger_y)
                    else:
                        drawing = False
                        last_finger_position = None
                elif mode == 'silgi':
                    canvas = np.zeros((480, 640, 3), dtype=np.uint8)
                    last_finger_position = None

        combined_frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
        cv2.imshow("Kalem ve Silgi", combined_frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
