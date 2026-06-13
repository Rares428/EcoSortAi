# Detector de reciclare (sticla / PET / doza)

Program care deschide camera web si detecteaza in timp real obiecte reciclabile
folosind YOLOv8.

## Instalare

```powershell
pip install -r requirements.txt
```

## Rulare rapida (model pre-antrenat COCO)

```powershell
python pet.py
```

Detecteaza bine **sticla / PET** (clasa `bottle`). Doza este doar aproximata
(COCO nu are clasa de doza). Pentru detectie corecta a dozelor -> antreneaza un
model propriu (mai jos).

Comenzi in fereastra: `q` = iesire, `s` = screenshot.

## Antrenare model propriu (sticla / PET / doza)

### 1. Obtine un dataset etichetat
Cel mai simplu, de pe [Roboflow Universe](https://universe.roboflow.com):

1. Cont gratuit pe https://roboflow.com
2. Cheia API: https://app.roboflow.com/settings/api
3. Descarca dataset-ul:
   ```powershell
   $env:ROBOFLOW_API_KEY = "cheia_ta"
   python download_data.py
   ```
   (Implicit: *Updated Recycling Dataset* cu clase PET, metal_can, glass_bottle. 
   Poti schimba workspace/project/version in `download_data.py` sau din linia de comanda.)

### 2. Antreneaza
```powershell
python train.py --data dataset/data.yaml --epochs 50 --imgsz 640
```
Pe CPU (cazul tau, fara placa video) e lent. Pentru un test rapid:
```powershell
python train.py --data dataset/data.yaml --epochs 30 --imgsz 416 --batch 8
```
Pentru antrenare rapida cu GPU gratuit, foloseste **Google Colab** (vezi mai jos).

### 3. Foloseste modelul antrenat
Dupa antrenare, modelul ajunge in `runs/detect/reciclare/weights/best.pt`.
`pet.py` il detecteaza si il foloseste **automat** la urmatoarea rulare:
```powershell
python pet.py
```

## Antrenare pe GPU gratuit (Google Colab) — recomandat
Calculatorul tau nu are GPU, deci antrenarea locala e lenta. Alternativ, in Colab:
```python
!pip install ultralytics roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="CHEIA_TA")
ds = rf.workspace("recyclestuff").project("updated-recycling-dataset").version(1).download("yolov8")
from ultralytics import YOLO
YOLO("yolov8n.pt").train(data=ds.location + "/data.yaml", epochs=50, imgsz=640)
```
Apoi descarca `best.pt` si pune-l in `runs/detect/reciclare/weights/best.pt` local.

## Fisiere
- `pet.py` — detectie live cu camera (alege automat modelul antrenat sau COCO)
- `download_data.py` — descarca dataset de pe Roboflow
- `train.py` — antreneaza modelul YOLO
- `requirements.txt` — dependinte
