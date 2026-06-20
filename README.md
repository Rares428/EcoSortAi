- This app detects recyclable objects (cans, plastic bottles and glass bottles)
- It can detect them live or on a folder with photos
- The program combines two models: YOLOv8 - COCO trained model and waste_best.pt - model trained for waste, overlapping detection is eliminated
- Installing in powershell: pip install -r requirements.txt
- Dependencies: `opencv-python`, `ultralytics`, `roboflow`
- Run live on camera: powershell --> python pet.py, commands: `q` = exit, `s` = screenshot (saved as `capture_N.jpg`).
- On a folder of images: Put the images (`.jpg`, `.jpeg`, `.png`, `.webp`) in the `test_images/` folder: powershell python test_poze.py
- The annotated images appear in `test_rezultate/`, and the console shows what was detected in each image.

Training your own model (for can detection)

- The COCO model does not know the "can" class, so detecting cans requires training your own model, saved as `waste_best.pt`.

### 1. Get a labeled dataset (Roboflow Universe)
1. Free account at https://roboflow.com
2. API key: https://app.roboflow.com/settings/api
3. Download the dataset:
   powershell --> $env:ROBOFLOW_API_KEY = "your_key"
   python download_data.py
   (Default: *Updated Recycling Dataset*, classes PET / metal_can / glass_bottle.
   You can change workspace/project/version in `download_data.py` or on the command line.)

### 2. Train
powershell --> python train.py --data dataset/data.yaml --epochs 50 --imgsz 640
On CPU (no GPU) it is slow. For a quick test:
powershell --> python train.py --data dataset/data.yaml --epochs 30 --imgsz 416 --batch 8
The result lands in `runs/detect/reciclare/weights/best.pt`. Rename it to
`waste_best.pt` (or adjust `pet.py`) so it is used for detection.

### Training on a free GPU (Google Colab) — recommended
See `reciclare_colab.ipynb`, or use directly:
python
!pip install ultralytics roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="YOUR_KEY")
ds = rf.workspace("recyclestuff").project("updated-recycling-dataset").version(1).download("yolov8")
from ultralytics import YOLO
YOLO("yolov8n.pt").train(data=ds.location + "/data.yaml", epochs=50, imgsz=640)
Then download `best.pt` and place it locally as `waste_best.pt`.

### Configuration
In `pet.py` you can tune:
- `CAMERA_INDEX` — camera index (0, 1, 2…) if the correct camera does not open;
- `CONF_MIN` — minimum confidence threshold for a detection (default `0.35`);
- `IOU_DEDUP` — overlap threshold above which two detections are considered the same object

-It is recomanded to be integreted in bigger system, but it canbe use alone
