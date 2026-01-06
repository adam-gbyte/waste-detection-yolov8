import json
import os
import shutil
import random

# ======================
# PATH
# ======================
ANNOTATION_FILE = "waste-detection-yolov8/annotations.json"
IMAGE_ROOT = "images"
OUTPUT = "dataset"

# ======================
# KELAS YOLO
# ======================
CLASS_MAP = {
    # plastic
    "Clear plastic bottle": 0,
    "Plastic bottle": 0,
    "Plastic bag": 0,
    "Plastic wrapper": 0,

    # paper
    "Paper": 1,
    "Carton": 1,

    # metal
    "Drink can": 2,
    "Aluminium foil": 2,
    "Metal bottle cap": 2,

    # glass
    "Glass bottle": 3,
    "Broken glass": 3,
    "Glass jar": 3,

    # organic
    "Food waste": 4,
    "Leaves": 4,

    # other
    "Battery": 5,
    "Plastic gloves": 5,
    "Shoe": 5
}

# ======================
# SPLIT RATIO
# ======================
TRAIN_RATIO = 0.7
VAL_RATIO = 0.2

# ======================
# LOAD JSON
# ======================
with open(ANNOTATION_FILE) as f:
    coco = json.load(f)

images = {img["id"]: img for img in coco["images"]}
categories = {cat["id"]: cat["name"] for cat in coco["categories"]}

annotations = {}
for ann in coco["annotations"]:
    img_id = ann["image_id"]
    cat_name = categories[ann["category_id"]]
    if cat_name not in CLASS_MAP:
        continue
    annotations.setdefault(img_id, []).append((ann, CLASS_MAP[cat_name]))

# ======================
# CREATE FOLDERS
# ======================
for split in ["train", "val", "test"]:
    os.makedirs(f"{OUTPUT}/images/{split}", exist_ok=True)
    os.makedirs(f"{OUTPUT}/labels/{split}", exist_ok=True)

# ======================
# SPLIT DATA
# ======================
img_ids = list(annotations.keys())
random.shuffle(img_ids)

n = len(img_ids)
train_end = int(n * TRAIN_RATIO)
val_end = int(n * (TRAIN_RATIO + VAL_RATIO))

splits = {
    "train": img_ids[:train_end],
    "val": img_ids[train_end:val_end],
    "test": img_ids[val_end:]
}

# ======================
# CONVERT & COPY
# ======================
for split, ids in splits.items():
    for img_id in ids:
        img = images[img_id]
        img_path = os.path.join(IMAGE_ROOT, img["file_name"])
        shutil.copy(img_path, f"{OUTPUT}/images/{split}")

        label_path = os.path.join(
            OUTPUT, "labels", split,
            os.path.splitext(os.path.basename(img["file_name"]))[0] + ".txt"
        )

        with open(label_path, "w") as f:
            for ann, cls in annotations[img_id]:
                x, y, w, h = ann["bbox"]
                iw, ih = img["width"], img["height"]

                xc = (x + w / 2) / iw
                yc = (y + h / 2) / ih
                w /= iw
                h /= ih

                f.write(f"{cls} {xc} {yc} {w} {h}\n")
