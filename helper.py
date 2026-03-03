import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv() 
my_results = os.getenv("my_results")


def show(path):
    """
    this function is used to show the image jpg extention (raw images)
    """
    img_bgr = cv2.imread(path)

    if img_bgr is None:
        print("Error: Image not found or unable to read.")
    else:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        plt.imshow(img_rgb)
        plt.xticks([]), plt.yticks([]) 
        plt.show()
    
def extract_frames(video_path, output_folder):
    """
    this function is used to extract the frames from the video and save them as jpg images
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    frame_count = 0
    while True:
        ret , frame = cap.read()
        if not ret:
            break

        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"Frame extraction complete. Total frames saved: {frame_count}")

def hsv_mask(image_bgr):

    """
    convert image to hsv and apply mask to detect green color
    """

    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(image_hsv, (100,80,0), (130,255,255))
    
    output = cv2.bitwise_and(image_bgr, image_bgr, mask=mask1)
    kernel = np.ones((5,5),np.uint8)
    gradient = cv2.morphologyEx(output, cv2.MORPH_GRADIENT, kernel)
    # store_results("hsv_morphology" , my_results , gradient)
    contours, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_mask = np.zeros_like(mask1)
    min_area = 2000  #tunable parameter

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            cv2.drawContours(filtered_mask, [cnt], -1, 255, thickness=-1)

    masked_frame = np.zeros_like(image_hsv)
    masked_frame[filtered_mask > 0] = image_hsv[filtered_mask > 0]
    return masked_frame

def canny(image): 
    """
    this function detect edges
    """
    gray = cv2.cvtColor(image , cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray , (5,5) , 0)
    canny = cv2.Canny(blur , 50 , 150)
    # store_results("canny_edge_detection" , my_results , canny)
    return canny

def display_mask(image):
    """
    display the mask shape
    """
    height = image.shape[0]
    # Define the coordinates
    points = np.array([(300 , height) , (410 , height) , (410 , 550), (250, 410)] , dtype=np.int32)
    
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, [points], (255,255,255)) 

    plt.imshow(mask, cmap='gray')
    plt.title("Mask")
    plt.axis('off')
    plt.show()

def roi(image):
    h = image.shape[0]
    w = image.shape[1]
    points = np.array([[[int(w/5),h],[int((2/5) * w),int(h/5)],[int((3/5) * w),int(h/5)],[w-int(w/5),h]]])
  
    mask = np.zeros_like(image)
    
    cv2.fillPoly(mask, [points], (255,255,255)) 
    masked_image = cv2.bitwise_and(mask , image)
    # store_results("masked_image" , my_results , masked_image)
    return masked_image
    
def display_lines(image , lines, thickness=20):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1 , y1 , x2 , y2 = line.reshape(4)
            cv2.line(line_image , (x1 , y1) , (x2 , y2) , (255 , 0 , 0) , 10)
    return line_image

def draw_lanes_on_image(image, lines, color=(0, 255, 0), thickness=10, alpha=0.8, beta=1.0, gamma=0.0):
    """
    Draws Hough lines on top of the original image and returns the combined result.
    - image: original BGR image (from cv2.imread)
    - lines: output of cv2.HoughLinesP
    """
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), color, thickness)

    combined = cv2.addWeighted(image, alpha, line_image, beta, gamma)
    return combined    

def store_results(filename, output_path, result):
    """
    Save the result image into the specified output folder.
    The image will be written as <output_path>/<filename>.jpg.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created folder: {output_path}")

    frame_path = os.path.join(output_path, f"{filename}.jpg")
    cv2.imwrite(frame_path, result)
    print(f"Saved result image to: {frame_path}")
