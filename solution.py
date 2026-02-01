"""
Derin Mavi Line Follower Challenge

Bu dosyayı düzenleyerek kendi çizgi izleme algoritmanızı geliştirin!
Aşağıdaki solution() fonksiyonunu tamamlayın.

Başarılar!
"""

import cv2
import numpy as np


def solution(image, current_speed, current_steering):
    """  
    Args:
        image: Robotun kamerasından gelen 64x64 pixel BGR görüntü (numpy array)
               
        current_speed: Robotun mevcut hızı (float)
                      
        current_steering: Robotun mevcut direksiyon açısı (float, -1 ile 1 arası)
                         - -1: Tam sol
                         -  0: Düz
                         -  1: Tam sağ
    
    Returns:
        target_speed: Robotun hedef hızı (float)

        steering: Robotun hedef direksiyon açısı (float, -1 ile 1 arası)
    """
    
    # ============================================
    # ÇÖZÜMÜNÜZÜ BURAYA YAZIN
    # ============================================

    if not hasattr(solution, "last_error"):
        solution.last_error = 0.0

    # 1. Image Processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # 2. Find line center
    M = cv2.moments(thresh)

    # Default safe values
    target_speed = 2
    steering = 0.0

    if M["m00"] > 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        error = cx - 32

        # P Controller
        kp = 0.1
        kd = 0

        derivative = error - solution.last_error
        solution.last_error = error

        steering = (error * kp) + (derivative * kd)

        cv2.drawMarker(image, (cx, cy), (255, 0, 0), cv2.MARKER_CROSS, 5, 1)
        cv2.line(image, (cx, cy), (32, 32), (0, 0, 255), 1)
        # print("error", error, "cx", cx, "cy", cy)
        # print("steering", steering)

    return target_speed, steering
