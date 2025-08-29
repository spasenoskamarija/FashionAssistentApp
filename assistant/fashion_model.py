
# Verzija 1.0

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

# Verzija 2.0

# import torch
# from transformers import BlipProcessor, BlipForConditionalGeneration
# from sentence_transformers import SentenceTransformer, util
# from PIL import Image
# from ultralytics import YOLO
# from itertools import chain, combinations
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
# # Object detection model
# yolo_model = YOLO("yolov8s-seg.pt")
#
# # Mapping function
# CATEGORY_MAP = {
#     "top": [
#         "top", "long sleeve top", "crop top", "tank top", "t-shirt", "tee", "shirt",
#         "blouse", "camisole", "bustier", "corset", "peplum", "knit top",
#         "sweater", "hoodie", "turtleneck", "polo", "pullover", "jersey"
#     ],
#     "bottom": [
#         "pants", "trousers", "jeans", "shorts", "skirt", "leggings",
#         "joggers", "culottes", "capris", "chinos"
#     ],
#     "dress": [
#         "dress", "gown", "slip dress", "maxi dress", "mini dress", "sundress",
#         "evening dress", "bodycon dress", "wrap dress"
#     ],
#     "shoes": [
#         "shoes", "sneakers", "heels", "sandals", "boots", "oxfords",
#         "loafers", "trainers", "flats", "pumps"
#     ],
#     "accessories": [
#         "bag", "handbag", "backpack", "belt", "scarf", "cap", "hat", "beanie",
#         "necklace", "watch", "earrings", "bracelet", "ring", "glasses", "sunglasses"
#     ],
#     "outerwear": [
#         "jacket", "coat", "vest", "cardigan", "blazer", "windbreaker",
#         "overcoat", "poncho", "parka", "puffer"
#     ]
# }
#
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
# #
# def detect_clothing_objects(image_input):
#     if isinstance(image_input, str):
#         image = Image.open(image_input).convert("RGB")
#     else:
#         image = image_input
#     results = yolo_model(image, verbose=False)
#     names = yolo_model.model.names
#     if results and results[0].boxes is not None:
#         class_ids = results[0].boxes.cls.tolist()
#         labels = [names[int(cls_id)] for cls_id in class_ids]
#         return labels
#     return []
#
# def categorize_from_labels(labels):
#     result = {cat: [] for cat in CATEGORY_MAP}
#     for label in labels:
#         for key, val in CATEGORY_MAP.items():
#             if label.lower() in val:
#                 result[key].append(label)
#     return result
#
# def group_by_category(wardrobe_items):
#     categories = {
#         "top": [], "bottom": [], "dress": [], "shoes": [], "accessories": []
#     }
#     for item in wardrobe_items:
#         fine = item.fine_category.lower()
#         for cat in categories:
#             if cat in fine:
#                 categories[cat].append(item)
#     return categories
#
# def powerset(iterable, max_len=2):
#     s = list(iterable)
#     return chain.from_iterable(combinations(s, r) for r in range(min(len(s), max_len)+1))
#
#
# def categorize_from_caption(caption):
#     caption = caption.lower()
#     for category, keywords in CATEGORY_MAP.items():
#         for word in keywords:
#             if word in caption:
#                 return category
#     return "Unknown"


# Verzija 3.0
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from sentence_transformers import SentenceTransformer, util
from PIL import Image
from ultralytics import YOLO
from itertools import chain, combinations

# -----------------------------
# BLIP captioning
# -----------------------------
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

# -----------------------------
# SentenceTransformer (kept; used elsewhere)
# -----------------------------
# NOTE: 'business' е отстранет и е споен во 'elegant'
style_labels = ["casual", "elegant", "sporty", "boho", "grunge", "streetwear", "chic"]
embedder = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

# -----------------------------
# YOLO object detector
# -----------------------------
yolo_model = YOLO("yolov8s-seg.pt")

# -----------------------------
# Category mapping
# -----------------------------
CATEGORY_MAP = {
    "top": [
        "top", "long sleeve top", "crop top", "tank top", "t-shirt", "tee", "shirt",
        "blouse", "camisole", "bustier", "corset", "peplum", "knit top",
        "sweater", "hoodie", "turtleneck", "polo", "pullover", "jersey"
    ],
    "bottom": [
        "pants", "trousers", "jeans", "shorts", "skirt", "leggings",
        "joggers", "culottes", "capris", "chinos"
    ],
    "dress": [
        "dress", "gown", "slip dress", "maxi dress", "mini dress", "sundress",
        "evening dress", "bodycon dress", "wrap dress"
    ],
    "shoes": [
        "shoes", "sneakers", "heels", "sandals", "boots", "oxfords",
        "loafers", "trainers", "flats", "pumps"
    ],
    "accessories": [
        "bag", "handbag", "backpack", "belt", "scarf", "cap", "hat", "beanie",
        "necklace", "watch", "earrings", "bracelet", "ring", "glasses", "sunglasses"
    ],
    "outerwear": [
        "jacket", "coat", "vest", "cardigan", "blazer", "windbreaker",
        "overcoat", "poncho", "parka", "puffer"
    ]
}

# ============================================================
# Core helpers you already had (kept)
# ============================================================

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

# ============================================================
# NEW: CLIP Zero-shot Style Classifier (+ heuristics)
# ============================================================

from transformers import CLIPProcessor, CLIPModel
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14").to(_device)
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

# Користиме една вистина за листата на стилови (без 'business')
STYLE_LABELS = style_labels

STYLE_TEMPLATES = {
    "casual": [
        "a photo of a casual outfit",
        "a person wearing a casual look",
        "everyday casual clothing"
    ],
    "elegant": [
        "a photo of an elegant outfit",
        "a person in an elegant evening look",
        "formal refined fashion style",
        "professional office wear",      # поранешен 'business' context
        "a tailored elegant outfit",
        "business attire for office"     # текст prompt е ок, label останува 'elegant'
    ],
    "sporty": [
        "a sporty athleisure outfit",
        "a person in athletic wear",
        "sport style clothing"
    ],
    "boho": [
        "a bohemian outfit with flowy fabrics",
        "boho chic fashion",
        "bohemian style clothing"
    ],
    "grunge": [
        "a grunge outfit with edgy vibe",
        "90s grunge fashion",
        "dark, distressed grunge look"
    ],
    "streetwear": [
        "a streetwear outfit",
        "urban street style clothing",
        "hypebeast streetwear look"
    ],
    "chic": [
        "a chic and polished outfit",
        "minimalist chic fashion",
        "stylish chic look"
    ],
}

def clip_style_scores(image_pil: Image.Image) -> dict:
    prompts = []
    owners  = []
    for style, tmpls in STYLE_TEMPLATES.items():
        for t in tmpls:
            prompts.append(t)
            owners.append(style)

    inputs = clip_processor(text=prompts, images=image_pil, return_tensors="pt", padding=True).to(_device)
    with torch.no_grad():
        out = clip_model(**inputs)
        logits = out.logits_per_image[0]  # similarity to each prompt

    scores = {style: -1e9 for style in STYLE_LABELS}
    idx = 0
    for style, tmpls in STYLE_TEMPLATES.items():
        k = len(tmpls)
        scores[style] = torch.max(logits[idx:idx+k]).item()
        idx += k
    return scores

# Клучни зборови: 'business' зборовите пренасочени кон 'elegant' (и делумно 'chic')
STYLE_KEYWORDS = {
    "streetwear": {"hoodie", "sneakers", "cap", "baggy", "cargo", "tracksuit"},
    "sporty": {"leggings", "sports", "joggers", "running", "athletic"},
    "elegant": {
        "gown", "dress", "heels", "slip", "silk", "satin",
        "blazer", "suit", "trousers", "oxfords", "loafers", "shirt", "tie", "pumps", "tailored"
    },
    "boho": {"floral", "flowy", "maxi", "fringe", "bohemian"},
    "grunge": {"distressed", "ripped", "leather", "combat", "plaid"},
    "chic": {"monochrome", "minimalist", "tailored", "polished"},
    "casual": {"t-shirt", "jeans", "sneakers", "sweater"},
}

def heuristic_style_boost(yolo_labels: list[str], caption: str) -> dict:
    caption_lc = caption.lower()
    tokens = set(l.lower() for l in yolo_labels) | set(caption_lc.replace(",", " ").split())
    boost = {s: 0.0 for s in STYLE_LABELS}

    for style, kws in STYLE_KEYWORDS.items():
        hits = sum(1 for kw in kws if kw in tokens or kw in caption_lc)
        if hits:
            boost[style] += 0.3 * hits

    # комбинации (бизнис → елегант)
    if (("dress" in tokens) or ("gown" in tokens)) and (("heels" in tokens) or ("sandals" in tokens)):
        boost["elegant"] += 0.8; boost["chic"] += 0.4
    if (("hoodie" in tokens) or ("cap" in tokens)) and (("sneakers" in tokens) or ("trainers" in tokens)):
        boost["streetwear"] += 0.8
    if (("blazer" in tokens) or ("suit" in tokens)) and (("heels" in tokens) or ("oxfords" in tokens) or ("loafers" in tokens)):
        boost["elegant"] += 0.8; boost["chic"] += 0.3
    return boost

def normalize_style(label: str) -> str:
    """Map old labels to the current set; 'business' → 'elegant'."""
    if not label:
        return "casual"
    l = label.lower()
    if l == "business":
        return "elegant"
    return l

def predict_style(image_pil: Image.Image, caption: str, yolo_labels: list[str]) -> str:
    """
    Final style: CLIP score + small heuristic boost.
    Returns normalized label (business→elegant).
    """
    clip_scores = clip_style_scores(image_pil)
    heur = heuristic_style_boost(yolo_labels, caption)
    final = {s: clip_scores[s] + 0.5 * heur[s] for s in STYLE_LABELS}
    best = max(final, key=final.get)
    return normalize_style(best)
