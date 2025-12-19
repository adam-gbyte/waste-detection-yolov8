import json
import os
import requests
from tqdm import tqdm

ANNOTATION_FILE = "annotations.json"
IMAGE_DIR = "images"

os.makedirs(IMAGE_DIR, exist_ok=True)

with open(ANNOTATION_FILE, "r") as f:
    data = json.load(f)

images = data["images"]

for img in tqdm(images):
    url = img.get("flickr_url")
    file_name = img["file_name"]

    if url is None:
        continue

    save_path = os.path.join(IMAGE_DIR, file_name)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    if os.path.exists(save_path):
        continue

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
    except:
        print("Gagal download:", file_name)
