import cv2
import time
import argparse
from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(description="YOLOv8 OpenCV Real-Time Detection")
    parser.add_argument("--model", type=str, default="runs/detect/train/weights/last.pt", help="Path ke model .pt")
    parser.add_argument("--source", type=str, default="0", help="0=webcam, path video, atau RTSP URL")
    parser.add_argument("--conf", type=float, default=0.3, help="Confidence threshold")
    parser.add_argument("--imgsz", type=int, default=640, help="Ukuran input model")
    parser.add_argument("--save", action="store_true", help="Simpan output ke file video")
    return parser.parse_args()


def main():
    args = parse_args()

    # Load model
    print("[INFO] Loading model...")
    model = YOLO(args.model)

    # Open video source
    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"[ERROR] Tidak bisa membuka source: {args.source}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    # Optional video writer
    if args.save:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))
    else:
        out = None

    prev_time = 0

    print("[INFO] Mulai deteksi... Tekan ESC untuk keluar.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[INFO] Stream selesai atau gagal.")
            break

        # Inference
        results = model(frame, conf=args.conf, imgsz=args.imgsz, verbose=False)

        annotated = results[0].plot()

        # FPS calculation
        curr_time = time.time()
        fps_text = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time

        cv2.putText(
            annotated, f"FPS: {fps_text:.2f}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )

        cv2.imshow("YOLOv8 Detection", annotated)

        if out:
            out.write(annotated)

        key = cv2.waitKey(1) & 0xFF
        if key in [27, ord("q")]:  # ESC atau q
            break

    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()
    print("[INFO] Program selesai.")


if __name__ == "__main__":
    main()
