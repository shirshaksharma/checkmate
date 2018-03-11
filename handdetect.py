import cv2
import numpy as np


def apply_hist_mask(frame, hist):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 256], 1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    cv2.filter2D(dst, -1, disc, dst)

    ret, thresh = cv2.threshold(dst, 100, 255, 0)
    thresh = cv2.merge((thresh, thresh, thresh))

    cv2.GaussianBlur(dst, (3, 3), 0, dst)
    res = cv2.bitwise_and(frame, thresh)
    return res


images = cv2.VideoCapture(0)
while True:
    _, img = images.read()

    width = images.get(3)
    height = images.get(4)

    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    roi = np.zeros([1, 10, 3], hsv.dtype)

    hist = cv2.calcHist([roi], [0], None, [256], [0, 256])
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

    # Draw circle at the middle of the screen
    cv2.circle(img, (int(width / 2), int(height / 2)), 5, (255, 0, 0))

    cv2.imshow('img', apply_hist_mask(img, hist))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
images.release()
