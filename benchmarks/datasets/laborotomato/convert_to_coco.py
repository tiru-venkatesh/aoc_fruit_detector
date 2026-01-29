import os
import json
import xml.etree.ElementTree as ET
from PIL import Image

DATASET_ROOT = "PATH_TO_LABOROTOMATO"
IMG_DIR = os.path.join(DATASET_ROOT, "JPEGImages")
ANN_DIR = os.path.join(DATASET_ROOT, "Annotations")
OUTPUT_JSON = "laborotomato_coco.json"

categories = [
    {"id": 1, "name": "tomato"}
]

coco = {
    "images": [],
    "annotations": [],
    "categories": categories
}

ann_id = 1
img_id = 1

for xml_file in os.listdir(ANN_DIR):
    if not xml_file.endswith(".xml"):
        continue

    xml_path = os.path.join(ANN_DIR, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    filename = root.find("filename").text
    img_path = os.path.join(IMG_DIR, filename)

    if not os.path.exists(img_path):
        continue

    width, height = Image.open(img_path).size

    coco["images"].append({
        "id": img_id,
        "file_name": filename,
        "width": width,
        "height": height
    })

    for obj in root.findall("object"):
        name = obj.find("name").text.lower()
        if name != "tomato":
            continue

        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        w = xmax - xmin
        h = ymax - ymin

        coco["annotations"].append({
            "id": ann_id,
            "image_id": img_id,
            "category_id": 1,
            "bbox": [xmin, ymin, w, h],
            "area": w * h,
            "iscrowd": 0
        })
        ann_id += 1

    img_id += 1

with open(OUTPUT_JSON, "w") as f:
    json.dump(coco, f, indent=2)

print("COCO annotation saved:", OUTPUT_JSON)
