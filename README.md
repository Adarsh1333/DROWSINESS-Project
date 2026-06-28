# DROWSINESS-Project
# Driver Drowsiness Detection System

The Driver Drowsiness Detection System is a real-time computer vision application developed using **Python** and **OpenCV** to enhance road safety by detecting signs of driver fatigue. The system uses a webcam to continuously monitor the driver's face and eyes with Haar Cascade Classifiers. It tracks whether the driver's eyes are visible and measures the duration for which they remain closed.

If the driver's eyes are not detected continuously for more than **3 seconds**, the system identifies a potential drowsiness condition. It immediately displays a **"DROWSINESS DETECTED"** warning on the screen, highlights the display with a red border, and plays a continuous alarm sound to alert the driver. The alarm automatically stops once the eyes are detected again.

The project uses image processing techniques such as grayscale conversion, face detection, eye detection, and real-time video analysis. Threading is used to play the alarm without interrupting the video stream, ensuring smooth real-time performance.

This system demonstrates the practical application of computer vision in intelligent transportation and driver safety. Although Haar Cascade-based eye detection may be affected by lighting conditions, head movement, or glasses, it provides a lightweight and efficient solution suitable for learning, prototyping, and academic projects.

**Technologies Used:** Python, OpenCV, Haar Cascade Classifiers, Playsound, Threading, and NumPy.

**Applications:** Driver monitoring systems, fatigue detection, road safety, accident prevention, and computer vision-based surveillance projects.

This project highlights how real-time image processing can assist in reducing fatigue-related accidents by providing timely visual and audio alerts, thereby improving driver awareness and promoting safer driving practices.
