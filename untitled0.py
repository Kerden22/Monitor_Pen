import cv2
import mediapipe as mp
import numpy as np

# MediaPipe el tespiti
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Buton boyutları
genislik, yukseklik = 100, 50  # Buton boyutları
canvas = np.zeros((480, 640, 3), dtype=np.uint8)  # Çizim alanı (siyah)

# Buton koordinatları
kalem_button = (20, 20, genislik, yukseklik)  # (x, y, width, height)
silgi_button = (150, 20, genislik, yukseklik)  # (x, y, width, height)

# Kamerayı başlat
cap = cv2.VideoCapture(0)

# MediaPipe parmak ayarları
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    mode = 'kalem'  # Başlangıç modu kalem
    drawing = False  # Çizim durumu
    last_finger_position = None  # Son parmak pozisyonu

    while cap.isOpened():
        ret, cevir = cap.read()
        if not ret:
            break

        # Görüntüyü yatayda çevir ve BGR -> RGB yap
        cevir = cv2.flip(cevir, 1)
        rgb_cevir = cv2.cvtColor(cevir, cv2.COLOR_BGR2RGB)
        
        # El tespiti
        sonuc = hands.process(rgb_cevir)

        # Butonları çiz
        cv2.rectangle(cevir, kalem_button[:2], (kalem_button[0] + genislik, kalem_button[1] + yukseklik), (255, 0, 0), -1)  # Kalem butonu
        cv2.putText(cevir, "Kalem", (kalem_button[0] + 10, kalem_button[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.rectangle(cevir, silgi_button[:2], (silgi_button[0] + genislik, silgi_button[1] + yukseklik), (0, 255, 0), -1)  # Silgi butonu
        cv2.putText(cevir, "Silgi", (silgi_button[0] + 10, silgi_button[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # İşaret parmağı koordinatları (Eğer el tespit edilmişse)
        if sonuc.multi_hand_landmarks:
            for hand_landmarks in sonuc.multi_hand_landmarks:
                mp_drawing.draw_landmarks(cevir, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # İşaret parmağı ucu 
                index_finger_tip = hand_landmarks.landmark[8]
                height, width, _ = cevir.shape
                finger_x, finger_y = int(index_finger_tip.x * width), int(index_finger_tip.y * height)

                # Buton seçimi
                if (kalem_button[0] < finger_x < kalem_button[0] + genislik and
                    kalem_button[1] < finger_y < kalem_button[1] + yukseklik):
                    mode = 'kalem'  # Kalem seçildi
                elif (silgi_button[0] < finger_x < silgi_button[0] + genislik and
                      silgi_button[1] < finger_y < silgi_button[1] + yukseklik):
                    mode = 'silgi'  # Silgi seçildi

                # Çizim yapma veya silme
                if mode == 'kalem':
                    if last_finger_position is not None:
                        cv2.line(canvas, last_finger_position, (finger_x, finger_y), (255, 0, 0), 5)  # Mavi renk ile çizim
                    drawing = True
                elif mode == 'silgi' and drawing:
                    canvas = np.zeros((480, 640, 3), dtype=np.uint8)  # Silme işlemi (tüm alanı sıfırla)

                last_finger_position = (finger_x, finger_y)

        # Görüntüyü göster
        combined_frame = cv2.addWeighted(cevir, 0.5, canvas, 0.5, 0)  # Görüntüyü ve çizimi birleştir
        cv2.imshow('Kalem ve Silgi', combined_frame)

        # ESC ile çık
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Kamera ve pencereleri serbest bırak
cap.release()
cv2.destroyAllWindows()
