import cv2
import time
import threading
from playsound import playsound

alarm_running = False
alarm_thread = None


def alarm():
    global alarm_running
    while alarm_running:
        try:
            playsound("alarm.mp3")
        except Exception as e:
            print("Alarm Error:", e)
            break


def start_alarm():
    global alarm_running, alarm_thread

    if not alarm_running:
        alarm_running = True
        alarm_thread = threading.Thread(target=alarm, daemon=True)
        alarm_thread.start()


def stop_alarm():
    global alarm_running
    alarm_running = False

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_eye.xml"
)

if face_cascade.empty():
    print("Error loading face cascade.")
    exit()

if eye_cascade.empty():
    print("Error loading eye cascade.")
    exit()
    
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam.")
    exit()

# Camera settings
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

eye_closed_start = None
face_missing_start = None

DROWSY_TIME = 4  # seconds

font = cv2.FONT_HERSHEY_SIMPLEX

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(120, 120)
    )

    eyes_found = 0
    face_detected = False

    for (x, y, w, h) in faces:

        face_detected = True

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

        roi_gray = gray[y:y + h // 2, x:x + w]
        roi_color = frame[y:y + h // 2, x:x + w]

        eyes = eye_cascade.detectMultiScale(
          roi_gray,
         scaleFactor=1.15,
    minNeighbors=8,
    minSize=(30,30),
    maxSize=(90,90)
)
        eyes_found = len(eyes)

        for (ex, ey, ew, eh) in eyes:

            cv2.rectangle(
                roi_color,
                (ex, ey),
                (ex + ew, ey + eh),
                (0, 255, 0),
                2
            )

    
    if face_detected:

        face_missing_start = None

        if eyes_found == 0:

            if eye_closed_start is None:
                eye_closed_start = time.time()

            closed_time = time.time() - eye_closed_start

            cv2.putText(
                frame,
                f"Eyes Closed: {closed_time:.1f}s",
                (20, 40),
                font,
                0.8,
                (0, 0, 255),
                2
            )

            if closed_time >= DROWSY_TIME:

                cv2.rectangle(
                    frame,
                    (0, 0),
                    (frame.shape[1], frame.shape[0]),
                    (0, 0, 255),
                    5
                )

                cv2.putText(
                    frame,
                    "DROWSINESS DETECTED!",
                    (150, 200),
                    font,
                    1.2,
                    (0, 0, 255),
                    3
                )

                start_alarm()

        else:
            eye_closed_start = None
            stop_alarm()

    
    else:

        if face_missing_start is None:
            face_missing_start = time.time()

        elif time.time() - face_missing_start > 1:
            eye_closed_start = None
            stop_alarm()

    
    status = "AWAKE"
    color = (0, 255, 0)

    if eye_closed_start is not None:

        elapsed = time.time() - eye_closed_start

        if elapsed >= DROWSY_TIME:
            status = "DROWSY"
            color = (0, 0, 255)
        else:
            status = "EYES CLOSED"
            color = (0, 255, 255)

    cv2.putText(
        frame,
        f"Status: {status}",
        (20, 80),
        font,
        0.8,
        color,
        2
    )

    cv2.imshow("Driver Monitoring System", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break

stop_alarm()

cap.release()

cv2.destroyAllWindows()

