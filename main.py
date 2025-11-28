import cv2
import numpy as np
img = cv2.imread("input-1.jpeg")


gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
median_blurred = cv2.medianBlur(gray_img, 7)
edges = cv2.Canny(median_blurred, 140, 200)

kernel= np.ones((3,3), np.uint8)
img_dilation = cv2.dilate(edges, kernel, iterations=1)
cv2.imshow("Display window", img_dilation)
cv2.waitKey(0)
cv2.destroyAllWindows()