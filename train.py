"""
Antreneaza un model YOLO personalizat pentru reciclare (sticla / PET / doza).

Foloseste un dataset in format YOLOv8 (un folder cu 'data.yaml' + imagini/etichete).
Vezi README.md pentru cum obtii dataset-ul de pe Roboflow Universe.

Rulare:
    python train.py --data cale/catre/data.yaml
    python train.py --data dataset/data.yaml --epochs 50 --imgsz 640

Pe CPU (fara placa video) antrenarea e lenta. Recomandari pentru CPU:
    - foloseste modelul mic 'yolov8n.pt' (implicit)
    - imgsz mai mic (ex. 416) si epoci mai putine (ex. 30) ca test initial
Rezultatul (cel mai bun model) ajunge in: runs/detect/<nume>/weights/best.pt
"""

import argparse
from ultralytics import YOLO


def main():
    p = argparse.ArgumentParser(description="Antrenare model reciclare YOLO")
    p.add_argument("--data", required=True, help="Calea catre data.yaml al dataset-ului")
    p.add_argument("--model", default="yolov8n.pt", help="Model de pornire (transfer learning)")
    p.add_argument("--epochs", type=int, default=50, help="Numar de epoci")
    p.add_argument("--imgsz", type=int, default=640, help="Dimensiunea imaginii la antrenare")
    p.add_argument("--batch", type=int, default=8, help="Marime batch (scade daca ramai fara RAM)")
    p.add_argument("--name", default="reciclare", help="Numele rularii (folderul de rezultate)")
    args = p.parse_args()

    model = YOLO(args.model)
    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        name=args.name,
        patience=15,          # opreste devreme daca nu se mai imbunatateste
    )

    print("\nGata! Cel mai bun model: runs/detect/" + args.name + "/weights/best.pt")
    print("Programul pet.py il va folosi automat la urmatoarea rulare.")


if __name__ == "__main__":
    main()
