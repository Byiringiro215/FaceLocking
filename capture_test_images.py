"""Capture test images for evaluation."""
import utils.session
import cv2
import os
from pathlib import Path

def capture_images():
    camera_index = 2
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    os.makedirs("photos", exist_ok=True)
    
    names = ["BYIRINGIRO.E", "Delice", "Isaac"]
    
    print("Capture test images for evaluation")
    print("=" * 50)
    
    for idx, name in enumerate(names, 1):
        print(f"\n[{idx}/3] Capturing images for: {name}")
        print(f"Press SPACE to capture, Q to skip to next person")
        
        captured = 0
        while captured < 2:  # Capture 2 images per person
            ret, frame = cap.read()
            if not ret:
                print("Error reading frame")
                break
            
            cv2.putText(frame, f"{name} - Press SPACE to capture (Captured: {captured}/2)", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Capture Test Images", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Space
                filename = f"photos/{name.lower().replace('.', '').replace(' ', '_')}_test_{captured+1}.jpg"
                cv2.imwrite(filename, frame)
                print(f"  ✓ Saved: {filename}")
                captured += 1
            elif key == ord('q'):  # Q
                print(f"  Skipped {name}")
                break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n" + "=" * 50)
    print("Test image capture complete!")
    print("\nCaptured files:")
    for f in sorted(Path("photos").glob("*.jpg")):
        print(f"  - {f}")

if __name__ == "__main__":
    capture_images()
