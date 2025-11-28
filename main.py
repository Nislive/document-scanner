import cv2
import numpy as np
img = cv2.imread("input-1.jpeg")


gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
median_blurred = cv2.medianBlur(gray_img, 7)
edges = cv2.Canny(median_blurred, 140, 200)

kernel= np.ones((3,3), np.uint8)
img_dilation = cv2.dilate(edges, kernel, iterations=1)

contours, hierarchy = cv2.findContours(img_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

contours = sorted(contours, key=cv2.contourArea, reverse=True)

target_contour = None

for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    epsilon = 0.02*perimeter
    approx = cv2.approxPolyDP(contour, epsilon, True)

    if len(approx) == 4:
        target_contour=approx
        break

pts = target_contour.reshape(4,2)
rect = np.zeros((4,2), dtype="float32")

cv2.imshow("Display window", pts)
cv2.waitKey(0)
cv2.destroyAllWindows()