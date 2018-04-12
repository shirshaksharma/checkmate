import cv2
import numpy as np

# HSV range for detecting skin color
minH = 0
maxH = 13
minS = 70
maxS = 230
minV = 80
maxV = 255

# Minimum and Maximum HSVs to look for
HSV_MIN = np.array([minH, minS, minV], np.uint8)
HSV_MAX = np.array([maxH, maxS, maxV], np.uint8)


# Finds the largest contour of a image within the HSV range
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
    im2, contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Picking the largest contour
    largest_contour = 0
    largest_contour_area = 0

    if contours:
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > largest_contour_area:
                largest_contour_area = area
                largest_contour = cnt

    return [img, img_dilation, largest_contour]


# Finds the convex hull in an image's contour
def find_convex_hull(img, largest_contour):
    if largest_contour is 0:
        return 0

    # Find the hull and defects
    hull = cv2.convexHull(largest_contour, returnPoints=False)
    defects = cv2.convexityDefects(largest_contour, hull)

    all_detected_points = []
    start = 0
    end = 0
    far = 0
    try:
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(largest_contour[s][0])
            end = tuple(largest_contour[e][0])
            # Points farthest from the center of the contour
            # In this case, the finger tip is the farthest point
            far = tuple(largest_contour[f][0])
            all_detected_points.append(far)
            cv2.line(img, start, end, [0, 255, 0], 4)
            cv2.circle(img, far, 5, [0, 0, 255], -1)

    except AttributeError:
        # print("Shape not found")
        return 0

    return [start, end, far, all_detected_points]
