"""Test MediaPipe 0.10.32 API for face landmarks."""
import mediapipe as mp
import cv2
import numpy as np
from pathlib import Path

print(f"MediaPipe version: {mp.__version__}")
print(f"Available at top level: {[x for x in dir(mp) if not x.startswith('_')]}")

# Try to find FaceMesh
try:
    from mediapipe.tasks import vision
    print("✓ vision module imported")
    print(f"Vision contents: {[x for x in dir(vision) if 'Face' in x]}")
except Exception as e:
    print(f"✗ Failed to import vision: {e}")

# Try direct import of face_mesh
try:
    from mediapipe.python.solutions import face_mesh
    print("✓ face_mesh imported from solutions")
except Exception as e:
    print(f"✗ Failed: {e}")

# Try legacy approach
try:
    import mediapipe.python.solutions as solutions
    print("✓ solutions module imported")
    print(f"Solutions contents: {[x for x in dir(solutions) if not x.startswith('_')]}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Try the old way that should fail
try:
    import mediapipe as mp
    if hasattr(mp, 'solutions'):
        print("✓ mp.solutions exists")
    else:
        print("✗ mp.solutions does NOT exist")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*50)
print("Testing actual FaceMesh...")

try:
    from mediapipe.python.solutions import face_mesh
    from mediapipe.python.solutions.drawing_utils import draw_landmarks
    
    fm = face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    print("✓ FaceMesh initialized successfully!")
    
    # Test on a sample image
    test_image = "photos/byiringiroe_test_1.jpg"
    if Path(test_image).exists():
        img = cv2.imread(test_image)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = fm.process(rgb)
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            print(f"✓ Detected {len(landmarks.landmark)} face landmarks")
            print(f"  First landmark: {landmarks.landmark[0]}")
        else:
            print("✗ No landmarks detected")
    else:
        print(f"✗ Test image not found: {test_image}")
    
    fm.close()
    
except Exception as e:
    import traceback
    print(f"✗ Error: {e}")
    traceback.print_exc()
