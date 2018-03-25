import cv2
import numpy as np
import time

##########################################
# CONSTANTS
##########################################

# HSV range of human skin
minH = 0
maxH = 20
minS = 30
maxS = 150
minV = 60
maxV = 255

HSV_MIN = np.array([minH, minS, minV], np.uint8)
HSV_MAX = np.array([maxH, maxS, maxV], np.uint8)

# Font properties
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 500)
fontScale = 1
fontColor = (0, 0, 0)
lineType = 2

# ROI of the circle
hsv_hand = HSV_MIN


##########################################


# Adds a circle in the middle of the screen
# Returns the frame
def displayPoints(frame):
    modified_img = frame
    width = images.get(3)
    height = images.get(4)
    width_mid = int(width / 2)
    height_mid = int(height / 2)

    # Circle ROI
    circle_roi = modified_img[
                 width_mid - 10: width_mid + 10,
                 height_mid - 10: height_mid + 10]

    # Draw circle at the middle of the screen
    cv2.circle(modified_img, (width_mid, height_mid), 10, (255, 255, 255))
    # Draws a text
    cv2.putText(img,
                'Place your hand in front of the circle!',
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)

    return [modified_img, circle_roi]


# Open the video stream
images = cv2.VideoCapture(0)
startTime = time.time() % 60

while True:
    _, img = images.read()

    # Display the circle for 5 seconds
    if (time.time() - startTime) % 60 < 1:
        imgDisplayCircle = displayPoints(img)[0]
        cv2.imshow('img with circle', imgDisplayCircle)
        hsv_hand = cv2.cvtColor(displayPoints(img)[1], cv2.COLOR_BGR2HSV)
        print("HSV Hand", hsv_hand)

    # Display the window
    else:
        cv2.destroyWindow('img with circle')
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        imgHSVInRange = cv2.inRange(imgHSV, HSV_MIN, HSV_MAX)

        imgMedianBlur = cv2.medianBlur(imgHSVInRange, 5)
        kernel = np.ones([5, 5], np.uint8)
        imgDilation = cv2.dilate(imgMedianBlur, kernel, iterations=1)

        # Detecting contours
        ret, thresh = cv2.threshold(imgDilation, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(imgDilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow('img', img)
        cv2.imshow('Blur + Dilation', imgDilation)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
images.release()

#
#
#
# def apply_hist_mask(frame, hist):
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 256], 1)
#
#     disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
#     cv2.filter2D(dst, -1, disc, dst)
#
#     ret, thresh = cv2.threshold(dst, 100, 255, 0)
#     thresh = cv2.merge((thresh, thresh, thresh))
#
#     cv2.GaussianBlur(dst, (3, 3), 0, dst)
#     res = cv2.bitwise_and(frame, thresh)
#     return res
#
#
# images = cv2.VideoCapture(0)
# while True:
#     _, img = images.read()
#
#     width = images.get(3)
#     height = images.get(4)
#
#     grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     roi = np.zeros([1, 10, 3], hsv.dtype)
#
#     hist = cv2.calcHist([roi], [0], None, [256], [0, 256])
#     cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
#
#     # Draw circle at the middle of the screen
#     cv2.circle(img, (int(width / 2), int(height / 2)), 5, (255, 0, 0))
#
#     cv2.imshow('img', apply_hist_mask(img, hist))
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cv2.destroyAllWindows()
# images.release()
