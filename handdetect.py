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

def find_largest_contour(img, min_hsv, max_hsv):
    # Converts the frame to HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Gets only the pixels that are in the HSV range
    img_hsv_in_range = cv2.inRange(img_hsv, min_hsv, max_hsv)

    # Blur and dilate the image
    median_blur = cv2.medianBlur(img_hsv_in_range, 5)
    kernel = np.ones([5, 5], np.uint8)
    img_dilation = cv2.dilate(median_blur, kernel, 1)

    # Detecting the contours
    ret, thresh = cv2.threshold(img_dilation, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Picking the largest contour
        largest_contour = 0
        largest_contour_area = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > largest_contour_area:
                largest_contour_area = area
                largest_contour = cnt

        # Drawing the contour
        # cv2.drawContours(img, largest_contour, -1, (0, 255, 0), 3)
        return [img, img_dilation, largest_contour]


def find_convex_hull(img, largest_contour):
    hull = cv2.convexHull(largest_contour, returnPoints=False)
    defects = cv2.convexityDefects(largest_contour, hull)

    start = 0
    end = 0
    far = 0
    try:
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(largest_contour[s][0])
            end = tuple(largest_contour[e][0])
            far = tuple(largest_contour[f][0])
            cv2.line(img, start, end, [0, 255, 0], 4)
            cv2.circle(img, far, 5, [0, 0, 255], -1)

    except AttributeError:
        print("Shape not found")

    return [start, end, far]



def nothing(x):
    pass


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


def getMinMaxFromHSV(hsv_values):
    min_hsv = np.array(hsv_values[0], hsv_values[1], hsv_values[2])
    max_hsv = np.array(hsv_values[0], hsv_values[1], hsv_values[2])
    return min_hsv, max_hsv


# Open the video stream
images = cv2.VideoCapture(0)
startTime = time.time() % 60


# Slider
img = np.zeros((300, 512, 3), np.uint8)
cv2.namedWindow('image')

# Works well. Not on the wooden table
cv2.createTrackbar('H Min', 'image', 0, 179, nothing)
cv2.createTrackbar('H Max', 'image', 10, 179, nothing)
cv2.createTrackbar('S Min', 'image', 70, 255, nothing)
cv2.createTrackbar('S Max', 'image', 230, 255, nothing)
cv2.createTrackbar('V Min', 'image', 80, 255, nothing)
cv2.createTrackbar('V Max', 'image', 255, 255, nothing)

# cv2.createTrackbar('H Min', 'image', 0, 179, nothing)
# cv2.createTrackbar('H Max', 'image', 30, 179, nothing)
# cv2.createTrackbar('S Min', 'image', 60, 255, nothing)
# cv2.createTrackbar('S Max', 'image', 255, 255, nothing)
# cv2.createTrackbar('V Min', 'image', 20, 255, nothing)
# cv2.createTrackbar('V Max', 'image', 255, 255, nothing)


while True:
    _, img = images.read()

    # Display the circle for 5 seconds
    if (time.time() - startTime) % 60 < 1:
        imgDisplayCircle = displayPoints(img)[0]
        cv2.imshow('img with circle', imgDisplayCircle)
        roiHSV = cv2.cvtColor(displayPoints(img)[1], cv2.COLOR_BGR2HSV)
        firstPixel = roiHSV[0][0]
        hsv_hand = np.array([firstPixel[0], firstPixel[1], firstPixel[2]], np.uint8)

        # print(hsv_hand)
        # print("changed")

        # cv2.createTrackbar('H Min', 'image', hsv_hand[0], 179, nothing)
        # cv2.createTrackbar('H Max', 'image', 179, 179, nothing)
        # cv2.createTrackbar('S Min', 'image', hsv_hand[1], 255, nothing)
        # cv2.createTrackbar('S Max', 'image', 255, 255, nothing)
        # cv2.createTrackbar('V Min', 'image', hsv_hand[2], 255, nothing)
        # cv2.createTrackbar('V Max', 'image', 255, 255, nothing)

    # Display the window
    else:
        cv2.destroyWindow('img with circle')
        # imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # imgHSVInRange = cv2.inRange(imgHSV, HSV_MIN, HSV_MAX)
        #
        # imgMedianBlur = cv2.medianBlur(imgHSVInRange, 5)
        # kernel = np.ones([5, 5], np.uint8)
        # imgDilation = cv2.dilate(imgMedianBlur, kernel, 1)
        #
        # # Detecting contours
        # ret, thresh = cv2.threshold(imgDilation, 127, 255, 0)
        # im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #
        # if contours:
        #     # Picking the largest contour
        #     largestContourIndex = 0
        #     largestContourArea = 0
        #
        #     for cnt in contours:
        #         area = cv2.contourArea(cnt)
        #         if area > largestContourArea:
        #             largestContourArea = area
        #             largestContourIndex = cnt
        #
        #     # Drawing the contours
        #     cv2.drawContours(img, largestContourIndex, -1, (0, 255, 0), 3)
        #
        #     hull = cv2.convexHull(largestContourIndex, returnPoints=False)
        #     defects = cv2.convexityDefects(largestContourIndex, hull)
        #
        #     try:
        #         for i in range(defects.shape[0]):
        #             s, e, f, d = defects[i, 0]
        #             start = tuple(largestContourIndex[s][0])
        #             end = tuple(largestContourIndex[e][0])
        #             far = tuple(largestContourIndex[f][0])
        #             cv2.line(img, start, end, [0, 255, 0], 4)
        #             cv2.circle(img, far, 5, [0, 0, 255], -1)
        #
        #     except AttributeError:
        #         print("shape not found")

        img_largest_contour = find_largest_contour(img, HSV_MIN, HSV_MAX)[0]
        largest_contour = find_largest_contour(img, HSV_MIN, HSV_MAX)[2]
        img_blur_dilation = find_largest_contour(img, HSV_MIN, HSV_MAX)[1]
        cv2.imshow('Largest Contour', img_largest_contour)
        cv2.imshow('Blur + Dilation', img_blur_dilation)
        find_convex_hull(img, largest_contour)
        cv2.imshow('img', img)

        minH = cv2.getTrackbarPos('H Min', 'image')
        minS = cv2.getTrackbarPos('S Min', 'image')
        minV = cv2.getTrackbarPos('V Min', 'image')

        maxH = cv2.getTrackbarPos('H Max', 'image')
        maxS = cv2.getTrackbarPos('S Max', 'image')
        maxV = cv2.getTrackbarPos('V Max', 'image')

        HSV_MIN = np.array([minH, minS, minV], np.uint8)
        HSV_MAX = np.array([maxH, maxS, maxV], np.uint8)

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
