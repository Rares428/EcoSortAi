"""
Descarca un dataset de reciclare de pe Roboflow Universe in format YOLOv8.

PASI:
  1. Fa-ti cont gratuit pe https://roboflow.com  (poti folosi contul Google)
  2. Ia-ti cheia API: https://app.roboflow.com/settings/api  (Private API Key)
  3. Pune cheia intr-o variabila de mediu sau foloseste optiunea --key:

       # PowerShell:
       $env:ROBOFLOW_API_KEY = "cheia_ta"
       python download_data.py

     sau:
       python download_data.py --key cheia_ta

Dataset implicit: "Updated Recycling Dataset" (clase PET, metal_can, glass_bottle, etc.)
  https://universe.roboflow.com/recyclestuff/updated-recycling-dataset

Dupa descarcare vei avea un folder cu 'data.yaml'. Antreneaza cu:
    python train.py --data <folder>/data.yaml
"""

import argparse
import os
from roboflow import Roboflow

# Parametrii dataset-ului implicit de pe Roboflow Universe.
WORKSPACE = "recyclestuff"
PROJECT = "updated-recycling-dataset"
VERSION = 1  # schimba daca pe pagina dataset-ului e alta versiune


def main():
    p = argparse.ArgumentParser(description="Descarca dataset reciclare de pe Roboflow")
    p.add_argument("--key", default=os.environ.get("ROBOFLOW_API_KEY"),
                   help="Cheia API Roboflow (sau seteaza ROBOFLOW_API_KEY)")
    p.add_argument("--workspace", default=WORKSPACE)
    p.add_argument("--project", default=PROJECT)
    p.add_argument("--version", type=int, default=VERSION)
    args = p.parse_args()

    if not args.key:
        raise SystemExit(
            "Lipseste cheia API. Seteaza $env:ROBOFLOW_API_KEY sau foloseste --key.\n"
            "O obtii de la: https://app.roboflow.com/settings/api"
        )

    rf = Roboflow(api_key=args.key)
    project = rf.workspace(args.workspace).project(args.project)
    dataset = project.version(args.version).download("yolov8")

    print("\nDataset descarcat in:", dataset.location)
    print("Antreneaza cu:")
    print(f'    python train.py --data "{dataset.location}/data.yaml"')


if __name__ == "__main__":
    main()
