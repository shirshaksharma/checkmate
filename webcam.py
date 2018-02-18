import cv2

# Capture video from Camera 0
cap = cv2.VideoCapture(0)

# Haar cascade for detecting the face
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# Haar cascade for detecting eyes
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

# Display the video on an infinite-loop until a break condition
while True:

    # Read the video stream
    ret, frame = cap.read()
    # Read the video stream and changes to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    print(faces)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the two videos
    cv2.imshow("gray", frame)

    # If the user presses q, break out of the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()