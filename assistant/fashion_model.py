

# import torch
# from transformers import BlipProcessor, BlipForConditionalGeneration
# from sentence_transformers import SentenceTransformer, util
# from PIL import Image
#
# # Captioning model
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
# blip_model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
#
# # Style classification model
# embedder = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
# style_labels = ["casual", "elegant", "sporty", "boho", "grunge", "streetwear", "chic", "business"]
#
# # Mapping function
# CATEGORY_MAP = {
#     "top": ["shirt", "blouse", "tank top", "t-shirt", "top"],
#     "bottom": ["pants", "shorts", "jeans", "skirt"],
#     "dress": ["dress", "gown"],
#     "shoes": ["shoes", "sneakers", "heels", "sandals", "boots"],
#     "accessories": ["bag", "necklace", "watch", "earrings", "bracelet", "belt", "scarf"],
#     "outerwear": ["jacket", "coat", "vest", "hoodie", "cardigan"]
# }
#
# def describe_outfit(image_path_or_file):
#     if isinstance(image_path_or_file, str):
#         raw_image = Image.open(image_path_or_file).convert("RGB")
#     else:
#         raw_image = Image.open(image_path_or_file).convert("RGB")
#
#     inputs = processor(raw_image, return_tensors="pt").to(blip_model.device)
#     out = blip_model.generate(**inputs)
#     return processor.decode(out[0], skip_special_tokens=True)
#
# def classify_style_from_text(description):
#     desc_emb = embedder.encode(description, convert_to_tensor=True)
#     label_embs = embedder.encode(style_labels, convert_to_tensor=True)
#     sims = util.pytorch_cos_sim(desc_emb, label_embs)[0]
#     best_idx = torch.argmax(sims).item()
#     return style_labels[best_idx]
#
# def embed(text):
#     return embedder.encode(text, convert_to_tensor=True)
#
# def get_similarity(emb1, emb2):
#     return util.pytorch_cos_sim(emb1, emb2).item()
#
# def categorize_from_caption(caption):
#     caption = caption.lower()
#     for category, keywords in CATEGORY_MAP.items():
#         for word in keywords:
#             if word in caption:
#                 return category
#     return "Unknown"
#

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from sentence_transformers import SentenceTransformer, util
from PIL import Image
from ultralytics import YOLO
from itertools import chain, combinations

# Captioning model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

# Style classification model
embedder = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
style_labels = ["casual", "elegant", "sporty", "boho", "grunge", "streetwear", "chic", "business"]

# Object detection model
yolo_model = YOLO("yolov8s-seg.pt")

# Mapping function
CATEGORY_MAP = {
    "top": ["shirt", "blouse", "tank top", "t-shirt"],
    "bottom": ["pants", "shorts", "jeans", "skirt"],
    "dress": ["dress", "gown"],
    "shoes": ["shoes", "sneakers", "heels", "sandals", "boots"],
    "accessories": ["bag", "necklace", "watch", "earrings", "bracelet", "belt", "scarf"],
    "outerwear": ["jacket", "coat", "vest", "hoodie", "cardigan"]
}

def describe_outfit(image_path_or_file):
    if isinstance(image_path_or_file, str):
        raw_image = Image.open(image_path_or_file).convert("RGB")
    else:
        raw_image = Image.open(image_path_or_file).convert("RGB")

    inputs = processor(raw_image, return_tensors="pt").to(blip_model.device)
    out = blip_model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)

def classify_style_from_text(description):
    desc_emb = embedder.encode(description, convert_to_tensor=True)
    label_embs = embedder.encode(style_labels, convert_to_tensor=True)
    sims = util.pytorch_cos_sim(desc_emb, label_embs)[0]
    best_idx = torch.argmax(sims).item()
    return style_labels[best_idx]

def embed(text):
    return embedder.encode(text, convert_to_tensor=True)

def get_similarity(emb1, emb2):
    return util.pytorch_cos_sim(emb1, emb2).item()
#
def detect_clothing_objects(image_input):
    if isinstance(image_input, str):
        image = Image.open(image_input).convert("RGB")
    else:
        image = image_input
    results = yolo_model(image, verbose=False)
    names = yolo_model.model.names
    if results and results[0].boxes is not None:
        class_ids = results[0].boxes.cls.tolist()
        labels = [names[int(cls_id)] for cls_id in class_ids]
        return labels
    return []

def categorize_from_labels(labels):
    result = {cat: [] for cat in CATEGORY_MAP}
    for label in labels:
        for key, val in CATEGORY_MAP.items():
            if label.lower() in val:
                result[key].append(label)
    return result

def group_by_category(wardrobe_items):
    categories = {
        "top": [], "bottom": [], "dress": [], "shoes": [], "accessories": []
    }
    for item in wardrobe_items:
        fine = item.fine_category.lower()
        for cat in categories:
            if cat in fine:
                categories[cat].append(item)
    return categories

def powerset(iterable, max_len=2):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(min(len(s), max_len)+1))


def categorize_from_caption(caption):
    caption = caption.lower()
    for category, keywords in CATEGORY_MAP.items():
        for word in keywords:
            if word in caption:
                return category
    return "Unknown"
