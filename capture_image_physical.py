import cv2
from datetime import datetime

# Open the default camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not accessible")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Show live camera feed
    cv2.imshow("Camera Feed - Press 'c' to capture, 'q' to quit", frame)

    key = cv2.waitKey(1) & 0xFF

    # Press 'c' to capture image
    if key == ord('c'):
        filename = f"page.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")

    # Press 'q' to quit
    elif key == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
