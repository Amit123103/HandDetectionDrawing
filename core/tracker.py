import cv2
import mediapipe as mp
import math
import numpy as np

class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0):
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            h, w, c = img.shape
            for id, lm in enumerate(my_hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list

    def is_pinching(self, lm_list, threshold=40):
        if len(lm_list) < 9:
            return False, 0, 0
        
        # Index finger tip (8) and Thumb tip (4)
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        
        length = math.hypot(x2 - x1, y2 - y1)
        
        if length < threshold:
            return True, (x1 + x2) // 2, (y1 + y2) // 2
        return False, 0, 0

    def is_fist(self, lm_list):
        if len(lm_list) < 21:
            return False
        
        # Check if fingers are folded.
        # Tips: 8, 12, 16, 20. MCPs: 5, 9, 13, 17.
        # If tips are below MCPs (y coordinate is larger), it's likely a fist.
        # Note: This simple logic assumes hand is upright.
        
        fingers = []
        # Thumb: Tip (4) is to the left or right of IP (3) depending on hand.
        # For simplicity, we'll check other 4 fingers for now.
        if lm_list[8][2] > lm_list[6][2]: # Index
            fingers.append(1)
        if lm_list[12][2] > lm_list[10][2]: # Middle
            fingers.append(1)
        if lm_list[16][2] > lm_list[14][2]: # Ring
            fingers.append(1)
        if lm_list[20][2] > lm_list[18][2]: # Pinky
            fingers.append(1)
            
        return len(fingers) == 4

class HeadTracker:
    def __init__(self, detection_confidence=0.7, tracking_confidence=0.5):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_head_pose(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(img_rgb)
        
        h, w, c = img.shape
        face_2d = []
        face_3d = []
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx in [33, 263, 1, 61, 291, 199]:
                        if idx == 1:
                            nose_2d = (lm.x * w, lm.y * h)
                            nose_3d = (lm.x * w, lm.y * h, lm.z * 3000)
                        
                        x, y = int(lm.x * w), int(lm.y * h)
                        face_2d.append([x, y])
                        face_3d.append([x, y, lm.z])
                
                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)
                
                # Camera matrix
                focal_length = 1 * w
                cam_matrix = np.array([ [focal_length, 0, w / 2],
                                        [0, focal_length, h / 2],
                                        [0, 0, 1]])
                # Distortion matrix
                dist_matrix = np.zeros((4, 1), dtype=np.float64)
                
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
                
                rmat, jac = cv2.Rodrigues(rot_vec)
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
                
                x_angle = angles[0] * 360
                y_angle = angles[1] * 360
                
                return x_angle, y_angle # Pitch (Up/Down), Yaw (Left/Right)
        return None, None
