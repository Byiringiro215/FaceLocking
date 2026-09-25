"""
Eye Detection-based blink tracking using brightness changes.
This is a practical workaround when MediaPipe is unavailable.
Uses synthetic eye region analysis based on face geometry.
"""
import cv2
import numpy as np


class EyeBlinkDetector:
    """Detect eye state and blinks using brightness changes in synthetic eye regions."""
    
    def __init__(self, ear_threshold=0.21, blink_min_frames=2, blink_max_frames=7):
        self.ear_threshold = ear_threshold
        self.blink_min_frames = blink_min_frames
        self.blink_max_frames = blink_max_frames
        
        self.low_ear_frames = 0
        self.last_brightness = None
        self.brightness_history = []
        self.blink_detected = False
        self.cascade_loaded = True  # We don't use cascades, but synthetic method
        
        print("[EyeBlinkDetector] Using brightness-based synthetic eye detection")
        
    def detect_blink(self, frame, face_box):
        """
        Detect blink by monitoring brightness changes in synthetic eye regions.
        
        Args:
            frame: Image frame
            face_box: (x, y, width, height) from YuNet
            
        Returns:
            dict with 'ear', 'blink', 'eyes_closed'
        """
        x, y, w, h = face_box
        x, y, w, h = int(x), int(y), int(w), int(h)
        
        # Validate face region
        if y < 0 or x < 0 or y + h > frame.shape[0] or x + w > frame.shape[1]:
            return {'ear': 0.5, 'blink': False, 'eyes_closed': False}
        
        # Extract face region
        roi = frame[y:y+h, x:x+w]
        if roi.size == 0:
            return {'ear': 0.5, 'blink': False, 'eyes_closed': False}
        
        try:
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            return {'ear': 0.5, 'blink': False, 'eyes_closed': False}
        
        # Estimate eye regions based on face geometry
        # Eyes are typically 1/3 down from top, 1/3 from left and 2/3 from left
        face_h, face_w = gray.shape[:2]
        
        # Left eye region (1/4 to 1/2 horizontally, 1/4 to 1/3 vertically)
        left_eye_y = int(face_h * 0.25)
        left_eye_y2 = int(face_h * 0.40)
        left_eye_x = int(face_w * 0.15)
        left_eye_x2 = int(face_w * 0.45)
        
        # Right eye region (1/2 to 3/4 horizontally, 1/4 to 1/3 vertically)
        right_eye_x = int(face_w * 0.55)
        right_eye_x2 = int(face_w * 0.85)
        right_eye_y = left_eye_y
        right_eye_y2 = left_eye_y2
        
        # Extract and analyze eye regions
        try:
            left_eye = gray[left_eye_y:left_eye_y2, left_eye_x:left_eye_x2]
            right_eye = gray[right_eye_y:right_eye_y2, right_eye_x:right_eye_x2]
            
            # Calculate average brightness (lower = eyes closed)
            left_brightness = np.mean(left_eye) if left_eye.size > 0 else 128
            right_brightness = np.mean(right_eye) if right_eye.size > 0 else 128
            avg_brightness = (left_brightness + right_brightness) / 2
            
        except Exception as e:
            return {'ear': 0.5, 'blink': False, 'eyes_closed': False}
        
        # Track brightness history for blink detection
        self.brightness_history.append(avg_brightness)
        if len(self.brightness_history) > 10:
            self.brightness_history.pop(0)
        
        # Estimate EAR from brightness (normalized 0-1)
        # High brightness = eyes open (high EAR), low brightness = eyes closed (low EAR)
        ear = min(avg_brightness / 255.0, 1.0)
        
        # Detect blink: brightness drops then recovers
        if self.last_brightness is not None:
            brightness_drop = self.last_brightness - avg_brightness
            
            # Blink threshold: significant brightness drop
            if brightness_drop > 30:  # Eyes closing
                self.low_ear_frames += 1
            elif self.low_ear_frames > 0 and brightness_drop < -20:  # Eyes recovering
                if self.blink_min_frames <= self.low_ear_frames <= self.blink_max_frames:
                    self.blink_detected = True
                else:
                    self.blink_detected = False
                self.low_ear_frames = 0
            elif self.low_ear_frames > self.blink_max_frames:
                # Reset if eye closing lasts too long (not a blink)
                self.low_ear_frames = 0
                self.blink_detected = False
        
        self.last_brightness = avg_brightness
        
        # Eyes are closed if brightness is very low
        eyes_closed = avg_brightness < 80
        
        return {
            'ear': ear,
            'blink': self.blink_detected,
            'eyes_closed': eyes_closed,
            'brightness': avg_brightness
        }
