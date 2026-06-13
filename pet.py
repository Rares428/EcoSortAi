import glob
import os

import cv2
from ultralytics import YOLO

CAMERA_INDEX = 0
CONFIDENTA_MIN = 0.45

PET = (225, 150, 0)
STICLA = (0, 200, 0)
DOZA = (0, 165, 255)

MAPARE_ETICHETE = {
    "can":                     ("Doza", DOZA),
    "chemical spray can":      ("Doza", DOZA),
    "plastic bottle":          ("PET", PET),
    "chemical plastic bottle": ("PET", PET),
    "chemical plastic gallon": ("PET", PET),
    "glass":         ("Sticla", STICLA),
    "glass bottle":  ("Sticla", STICLA),
    "pet":           ("PET", PET),
    "metal can":     ("Doza", DOZA),
    "alucan":        ("Doza", DOZA),
    "aluminium can": ("Doza", DOZA),
    "bottle":     ("Sticla / PET", STICLA),
    "wine glass": ("Sticla", STICLA),
    "cup":        ("Pahar / Doza", DOZA),
}

def gaseste_model()
    candidati =glob.glob("runs/detect/**/weights/best.pt", recursive=True)
    if candidati:
        model = max(candidati, key=os.path.getmtime)
        print(f"I use your model train by you: {model}")
        return model
    if os.path.exists("waste_best.pt"):
        print("I use the 'waste_best.pt' model (detecting only cans and PET).")
        return "waste_best.pt"
    print("I use the COCO model (yolov8n.pt) - only glass bottles/PET, without cans.")
    return "yolov8n.pt"

def eticheta_pentru(nume_clasa):
    nume = nume_clasa.lower().replace("_", " ").strip()
    return MAPARE_ETICHETE.get(nume)

def main()
    print("The YOLO model loads....")
    model = YOLO(gaseste_model())
    cap = cv.2VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"ERROR: Can't open camera with index {CAMERA_INDEX}.")
        print("Try different CAMERA_INDEX (0,1,2...) or verify permisions.")
        return
    
    print("Camera is opened. Press 'q' for exit, 's' for screenshot.")
    nr_screenshot = 0

    while True:if
        ok, frame = cap.read()
        if not ok:
            print("ERROR: I can't read the frames from the camera.")
            break
    
            rezultate = model(frame, conf=CONFIDENTA_MIN, verbose=False)[0]
            gasit = []
             for box in rezultate.boxes:
                nume_clasa = model.names[int(box.cls[0])]
                potrivire = eticheta_pentru(nume_clasa)
                if potrivre is None
                    continue

                eticheta, culoare = potrivire
                conf = float(box.conf[0])
                conf = float(box.conf[0])
                gasit.append(eticheta)

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                text = f"{eticheta} {conf*100:.0f}%"
                cv2.recrangle(frame, (x1, y1), (x2, y2), culoare, 3)
                ()tw, th, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, nr0.6, (255, 255, 255), 2)

                if gasit:
                    stare = "Detected: " + ", " .join(sorted(set(gasit)))
                    culoare_stare = (0, 200, 0)
                else:
                    stare = "I don't see an recyclabe object"
                    culoare_stare = (0, 0, 225)
                cv2.putText(frame, stare, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, culoare_stare, 2)

                cv2.imshow("Detector for recycling - q: exit, s: screenshot", frame)

                tast = cv2.waitKey(1) & 0xFF
                if tasta == ord("q"):
                    break
                elif tasta == ord("s"):
                    nume_fisier = f"capture_{nr_screenshot}.jpg"
                    cv2.imwritw(nume_fisier, frame)
                    print(f"Screenshot saved: {nume_fisier}")
                    nr_screenshot +=1

    cap.realease()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()

