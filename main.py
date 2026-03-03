import math
import cv2 
from helper import*
import os
from dotenv import load_dotenv
load_dotenv() 
video_path = os.getenv("video_path")

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
h, w, _ = frame.shape
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (w, h))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv_image = hsv_mask(frame)
    canny_image = canny(hsv_image)
    cropped_image = roi(canny_image)

    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]),
                            minLineLength=50, maxLineGap=35)

    #vertical lines filter
    vertical_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            degrees = math.degrees(math.atan2(y2 - y1, x2 - x1)) % 360
            if (70 <= degrees <= 110) or (250 <= degrees <= 290):
                vertical_lines.append(line)

    vertical_lines = np.array(vertical_lines) if vertical_lines else None

    line_image = display_lines(frame, vertical_lines)
    result = draw_lanes_on_image(frame, vertical_lines)

    cv2.imshow('Lane Detection', result)
    out.write(result)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
cv2.waitKey(1)