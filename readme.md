# 🏊‍♂️ Underwater Lane Detection & Drift Analysis

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)

A computer vision-based system designed to track swimming pool lane markers and assist swimmers in maintaining a straight path. This project leverages advanced image processing to identify pool floor geometry under challenging underwater conditions.

---

## 🚀 Version 1.0: Core Detection
The current release focuses on **robust feature extraction** and **lane identification**.

### Key Features:
* **Lane Segmentation:** Detection of floor tiles and lane boundaries using color-space filtering (HSV/LAB) and Canny edge detection.
* **Geometric Fitting:** Utilizes Hough Transforms to track the linear path of the pool floor markers.
* **Visual Overlay:** Real-time green-line rendering to confirm detection accuracy and stability.

---

## 🛠 Deployment & Data Enhancement
This project is built for real-world application, emphasizing performance and visual clarity.

### Deployment Method
* **Modular Architecture:** The detection logic is decoupled from the visualization layer, allowing for easy integration into mobile apps or embedded hardware.
* **Stream Processing:** Optimized to handle both high-resolution `.mp4` files and low-latency live RTSP camera feeds.

### Data Enhancement Pipeline
* **Preprocessing:** Includes Gaussian blurring to reduce "salt and pepper" noise caused by bubbles.
* **ROI Masking:** Focuses processing power on the bottom half of the frame to ignore surface reflections and splashes.
* **Contrast Stretching:** Normalizes the "blue-heavy" underwater spectrum to make lane markers pop against the pool floor.

---

## 📈 Future Work: Version 2.0 (The "Drift" Update)
The next evolution of this project moves from passive detection to active navigation.

### 1. Drift Detection (Departure Warning)
* **Centerline Tracking:** Establishing a mathematical "Zero Point" based on the detected lane center.
* **Offset Calculation:** Real-time measurement of the distance between the camera center and the lane's geometric center.
* **Visual Alerts:** The UI will transition from green to red when the calculated drift exceeds a specific safety threshold.



### 2. Environmental Robustness
* **Temporal Smoothing:** Implementing Kalman Filters to prevent "flickering" when the view is momentarily obstructed.
* **Atmospheric Correction:** Algorithmic "De-hazing" to improve visibility in murky or highly chlorinated water.


