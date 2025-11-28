import cv2
import numpy as np
import math
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

plus = np.sum(pts, axis=1)
diff = np.diff(pts, axis=1)


rect = np.array([
                pts[np.argmin(plus)],
                pts[np.argmin(diff)],
                pts[np.argmax(plus)],
                pts[np.argmax(diff)]
                ], dtype="float32")

(tl, tr, br, bl) =  rect 

widthA = math.dist(tl, tr)
widthB = math.dist(bl, br)
maxWidth=max(int(widthA), int(widthB))


heightA = math.dist(tl, bl)
heightB = math.dist(tr, br)

#for A4
maxHeight = int(maxWidth * 1.414)

input_pts = rect
output_pts = np.float32([
    [0, 0],
    [maxWidth, 0],
    [maxWidth, maxHeight],
    [0, maxHeight]
])
M = cv2.getPerspectiveTransform(input_pts, output_pts)

out = cv2.warpPerspective(img, M, (maxWidth, maxHeight))

cv2.imshow("Display window", out)
cv2.waitKey(0)
cv2.destroyAllWindows()