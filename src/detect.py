import cv2
import sys


CAMERA_INDEX = 2


def main():
    print("[DEBUG] Starting face detection...")
    print(f"[DEBUG] Camera index: {CAMERA_INDEX}")
    
    detector_path = (
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    print(f"[DEBUG] Haar cascade path: {detector_path}")
    
    detector = cv2.CascadeClassifier(detector_path)

    if detector.empty():
        raise RuntimeError(
            f"Could not load Haar detector: {detector_path}"
        )
    
    print("[DEBUG] ✓ Haar cascade loaded successfully")

    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera {CAMERA_INDEX}.")
    
    print("[DEBUG] ✓ Camera opened successfully")
    
    # Get camera properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"[DEBUG] Camera resolution: {frame_width}x{frame_height} @ {fps} FPS")

    print("Face detection running. Press 'q' to quit.")
    
    frame_count = 0
    faces_total = 0

    while True:
        frame_count += 1
        ok, frame = cap.read()

        if not ok:
            print("[DEBUG] Failed to read frame")
            break

        if frame is None:
            print("[DEBUG] Frame is None")
            break

        print(f"\r[DEBUG] Frame {frame_count}: shape={frame.shape}", end="", flush=True)

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY,
        )
        
        print(f", gray shape={gray.shape}", end="", flush=True)

        faces = detector.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(50, 50),
        )
        
        print(f", faces found={len(faces)}", end="", flush=True)
        faces_total += len(faces)

        for x, y, w, h in faces:
            print(f" [FACE at ({x},{y}) {w}x{h}]", end="", flush=True)
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2,
            )
        
        # Add text to frame
        cv2.putText(frame, f"Faces: {len(faces)}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Frame: {frame_count}", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Face Detection", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print(f"\n[DEBUG] Quit pressed")
            break

    print(f"\n[DEBUG] Stopped. Processed {frame_count} frames, found {faces_total} faces total")
    cap.release()
    cv2.destroyAllWindows()
    print("[DEBUG] ✓ Resources cleaned up")


if __name__ == "__main__":
    main()