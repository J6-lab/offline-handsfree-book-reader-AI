import cv2
import mediapipe as mp
import pyautogui
import sys
import time
import os
from collections import deque
import math

# ================= ACCESSIBILITY CONFIG =================
SCROLL_AMOUNT = 70
SCROLL_DELAY = 0.45
SMOOTHING_FRAMES = 4

# Relative vertical thresholds (elderly + young friendly)
UP_THRESHOLD = -0.015
DOWN_THRESHOLD = 0.015

# Blink → return to main menu
EAR_THRESHOLD = 0.19
BLINK_EXIT_COUNT = 6
BLINK_WINDOW = 3.0

# Horizontal → terminate program
HORIZONTAL_DELTA = 0.04
HORIZONTAL_EXIT_COUNT = 4
# ========================================================

file_path = sys.argv[1]

# Open document
os.startfile(file_path)
time.sleep(3)

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

eye_y_history = deque(maxlen=SMOOTHING_FRAMES)
eye_x_history = deque(maxlen=5)

baseline_eye_y = None
last_scroll_time = time.time()

blink_times = deque()
horizontal_count = 0
last_horizontal_dir = None

# Eye landmarks
LEFT_EYE_Y = [159, 145]
RIGHT_EYE_Y = [386, 374]

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(lm, ids):
    p = [lm[i] for i in ids]
    v1 = math.dist((p[1].x, p[1].y), (p[5].x, p[5].y))
    v2 = math.dist((p[2].x, p[2].y), (p[4].x, p[4].y))
    h = math.dist((p[0].x, p[0].y), (p[3].x, p[3].y))
    return (v1 + v2) / (2.0 * h)

print("👀 Eye-Tracking Scroll ACTIVE")
print("Look UP / DOWN → Scroll")
print("Blink fast 6× → Main Menu")
print("Left–Right eyes → Exit Program")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = face_mesh.process(rgb)

    if res.multi_face_landmarks:
        lm = res.multi_face_landmarks[0].landmark
        now = time.time()

        # -------- STABLE EYE CENTER (KEY FIX) --------
        eye_center_y = (
            lm[LEFT_EYE_Y[0]].y + lm[LEFT_EYE_Y[1]].y +
            lm[RIGHT_EYE_Y[0]].y + lm[RIGHT_EYE_Y[1]].y
        ) / 4

        if baseline_eye_y is None:
            baseline_eye_y = eye_center_y

        eye_y_history.append(eye_center_y)
        avg_eye_y = sum(eye_y_history) / len(eye_y_history)
        delta_y = avg_eye_y - baseline_eye_y

        # -------- VERTICAL SCROLL (WORKING) --------
        if now - last_scroll_time > SCROLL_DELAY:
            if delta_y < UP_THRESHOLD:
                pyautogui.scroll(SCROLL_AMOUNT)
                last_scroll_time = now
            elif delta_y > DOWN_THRESHOLD:
                pyautogui.scroll(-SCROLL_AMOUNT)
                last_scroll_time = now

        # -------- BLINK → MAIN MENU --------
        ear = (
            eye_aspect_ratio(lm, LEFT_EYE) +
            eye_aspect_ratio(lm, RIGHT_EYE)
        ) / 2

        if ear < EAR_THRESHOLD:
            blink_times.append(now)

        while blink_times and now - blink_times[0] > BLINK_WINDOW:
            blink_times.popleft()

        if len(blink_times) >= BLINK_EXIT_COUNT:
            print("👁 Blink detected → returning to menu")
            cap.release()
            cv2.destroyAllWindows()
            sys.exit(2)

        # -------- HORIZONTAL → TERMINATE --------
        eye_x = lm[468].x
        eye_x_history.append(eye_x)

        if len(eye_x_history) == eye_x_history.maxlen:
            delta_x = eye_x_history[-1] - eye_x_history[0]

            if abs(delta_x) > HORIZONTAL_DELTA:
                direction = "RIGHT" if delta_x > 0 else "LEFT"
                if direction != last_horizontal_dir:
                    horizontal_count += 1
                    last_horizontal_dir = direction

            if horizontal_count >= HORIZONTAL_EXIT_COUNT:
                print("👀 Horizontal exit → program terminated")
                cap.release()
                cv2.destroyAllWindows()
                sys.exit(1)

        # -------- DEBUG OVERLAY --------
        cv2.putText(frame, f"dY: {delta_y:.4f}", (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Eye Tracking Scroll (Q to close window)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
sys.exit(0)
