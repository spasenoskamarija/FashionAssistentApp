# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .forms import UserRegisterForm, ProfileForm, ClothingItemForm
# from .models import ClothingItem
# from .fashion_model import (
#     describe_outfit, classify_style_from_text,
#     embed, get_similarity, categorize_from_caption
# )
# from itertools import product
# from PIL import Image
#
# def home(request):
#     return render(request, 'home.html')
#
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'registration/register.html', {'form': form})
#
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#         if form.is_valid():
#             profile = form.save()
#             if profile.profile_picture:
#                 image_path = profile.profile_picture.path
#                 description = describe_outfit(image_path)
#                 style = classify_style_from_text(description)
#                 profile.predicted_style = f"{description} ⟶ {style}"
#                 profile.save()
#             return redirect('profile')
#     else:
#         form = ProfileForm(instance=request.user.profile)
#
#     return render(request, 'profile.html', {
#         'form': form,
#         'profile': request.user.profile
#     })
#
# @login_required
# def wardrobe(request):
#     if request.method == 'POST':
#         form = ClothingItemForm(request.POST, request.FILES)
#         if form.is_valid():
#             item = form.save(commit=False)
#             item.profile = request.user.profile
#
#             description = describe_outfit(item.image)
#             item.description = description
#
#             style = classify_style_from_text(description)
#             item.predicted_style = style
#
#             item.fine_category = categorize_from_caption(description)
#             item.detected_labels = "BLIP-based"
#
#             item.save()
#             return redirect('wardrobe')
#     else:
#         form = ClothingItemForm()
#
#     items = ClothingItem.objects.filter(profile=request.user.profile)
#     return render(request, 'wardrobe.html', {'form': form, 'items': items})
#
# @login_required
# def delete_clothing(request, item_id):
#     item = get_object_or_404(ClothingItem, id=item_id, profile=request.user.profile)
#     item.delete()
#     return redirect('wardrobe')
#
# @login_required
# def suggest_outfit(request):
#     query = request.GET.get("q", "elegant outfit for party")
#     query_emb = embed(query)
#
#     wardrobe = request.user.profile.clothes.all()
#     combos = []
#     for combo in product(wardrobe, repeat=3):
#         desc = " ".join([f"{c.description} {c.predicted_style}" for c in combo])
#         desc_emb = embed(desc)
#         score = get_similarity(desc_emb, query_emb)
#         combos.append((score, combo))
#
#     combos.sort(key=lambda x: x[0], reverse=True)
#     combos = combos[:10]
#
#     return render(request, "suggest_outfit.html", {
#         "outfit_combos": combos
#     })
from django.db.models import Count
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .forms import UserRegisterForm, ProfileForm, ClothingItemForm
# from .models import ClothingItem
# from .fashion_model import (
#     describe_outfit, classify_style_from_text,
#     detect_clothing_objects, embed, get_similarity,
#     categorize_from_labels, group_by_category, powerset
# )
# from .models import UserOutfit
# from .forms import UserOutfitForm
# from itertools import product
# from PIL import Image
#
# def home(request):
#     return render(request, 'home.html')
#
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'registration/register.html', {'form': form})
#
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#         if form.is_valid():
#             profile = form.save()
#             if profile.profile_picture:
#                 image_path = profile.profile_picture.path
#                 description = describe_outfit(image_path)
#                 style = classify_style_from_text(description)
#                 profile.predicted_style = f"{description} ⟶ {style}"
#                 profile.save()
#             return redirect('profile')
#     else:
#         form = ProfileForm(instance=request.user.profile)
#
#     return render(request, 'profile.html', {
#         'form': form,
#         'profile': request.user.profile
#     })
#
# @login_required
# def wardrobe(request):
#     if request.method == 'POST':
#         form = ClothingItemForm(request.POST, request.FILES)
#         if form.is_valid():
#             item = form.save(commit=False)
#             item.profile = request.user.profile
#
#             description = describe_outfit(item.image)
#             item.description = description
#
#             style = classify_style_from_text(description)
#             item.predicted_style = style
#
#             image = Image.open(item.image).convert("RGB")
#             labels = detect_clothing_objects(image)
#             item.detected_labels = ', '.join(labels) if labels else 'None'
#
#             label_map = categorize_from_labels(labels)
#             categories = []
#             for key, values in label_map.items():
#                 if values:
#                     categories.append(key)
#
#             item.fine_category = ", ".join(categories) if categories else "Unknown"
#
#             item.save()
#             return redirect('wardrobe')
#     else:
#         form = ClothingItemForm()
#
#     items = ClothingItem.objects.filter(profile=request.user.profile)
#     return render(request, 'wardrobe.html', {'form': form, 'items': items})
#
# @login_required
# def delete_clothing(request, item_id):
#     item = get_object_or_404(ClothingItem, id=item_id, profile=request.user.profile)
#     item.delete()
#     return redirect('wardrobe')
#
# @login_required
# def suggest_outfit(request):
#     query = request.GET.get("q", "").strip()
#     if not query:
#         return render(request, "suggest_outfit.html", {
#             "outfit_combos": [],
#             "message": "Please enter a style to generate outfit suggestions."
#         })
#
#     query_emb = embed(query)
#     wardrobe = request.user.profile.clothes.all()
#
#     if not wardrobe:
#         return render(request, "suggest_outfit.html", {
#             "outfit_combos": [],
#             "message": "No clothing items found in your wardrobe."
#         })
#
#     grouped = group_by_category(wardrobe)
#     combos = []
#
#     # Combo: dress + accessories
#     for dress in grouped["dress"]:
#         for acc_combo in powerset(grouped["accessories"], max_len=2):
#             combo = [dress] + list(acc_combo)
#             desc = " ".join(f"{i.description} {i.predicted_style}" for i in combo)
#             score = get_similarity(embed(desc), query_emb)
#             combos.append((score, combo))
#
#     # Combo: top + bottom (+ shoes) (+ accessories)
#     for top in grouped["top"]:
#         for bottom in grouped["bottom"]:
#             for shoes in [None] + grouped["shoes"]:
#                 for acc_combo in powerset(grouped["accessories"], max_len=2):
#                     combo = [top, bottom]
#                     if shoes: combo.append(shoes)
#                     combo.extend(acc_combo)
#                     desc = " ".join(f"{i.description} {i.predicted_style}" for i in combo)
#                     score = get_similarity(embed(desc), query_emb)
#                     combos.append((score, combo))
#
#     combos.sort(key=lambda x: x[0], reverse=True)
#     combos = combos[:10]
#
#     return render(request, "suggest_outfit.html", {
#         "outfit_combos": combos,
#         "query": query
#     })
#
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserOutfitForm(request.POST, request.FILES)
#         if form.is_valid():
#             outfit = form.save(commit=False)
#             outfit.profile = request.user.profile
#
#             # Caption + Style
#             description = describe_outfit(outfit.image)
#             style = classify_style_from_text(description)
#             outfit.description = description
#             outfit.predicted_style = style
#
#             # YOLO категории
#             image = Image.open(outfit.image).convert("RGB")
#             labels = detect_clothing_objects(image)
#             outfit.detected_labels = ', '.join(labels) if labels else 'None'
#
#             label_map = categorize_from_labels(labels)
#             categories = [key for key, val in label_map.items() if val]
#             outfit.fine_category = ", ".join(categories) if categories else "Unknown"
#
#             outfit.save()
#             return redirect('profile')
#     else:
#         form = UserOutfitForm()
#
#     outfits = request.user.profile.user_outfits.all()
#
#     return render(request, 'profile.html', {
#         'form': form,
#         'profile': request.user.profile,
#         'outfits': outfits
#     })
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm, ClothingItemForm, UserOutfitForm
from .models import ClothingItem, UserOutfit
from .fashion_model import (
    describe_outfit, classify_style_from_text,
    detect_clothing_objects, embed, get_similarity,
    categorize_from_labels, group_by_category, powerset, categorize_from_caption
)
from itertools import product
from PIL import Image


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        outfit_form = UserOutfitForm(request.POST, request.FILES)

        if form.is_valid():
            profile = form.save()
            if profile.profile_picture:
                image_path = profile.profile_picture.path
                description = describe_outfit(image_path)
                style = classify_style_from_text(description)
                profile.predicted_style = f"{description} ⟶ {style}"
                profile.save()
            return redirect('profile')

        if outfit_form.is_valid():
            outfit = outfit_form.save(commit=False)
            outfit.profile = profile

            description = describe_outfit(outfit.image)
            style = classify_style_from_text(description)
            outfit.description = description
            outfit.predicted_style = style

            image = Image.open(outfit.image).convert("RGB")
            labels = detect_clothing_objects(image)
            outfit.detected_labels = ', '.join(labels) if labels else 'None'

            label_map = categorize_from_labels(labels)
            categories = [key for key, val in label_map.items() if val]
            outfit.fine_category = ", ".join(categories) if categories else "Unknown"

            outfit.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
        outfit_form = UserOutfitForm()

    outfits = profile.user_outfits.all()
    favorites = outfits.filter(favorite=True)
    non_favorites = outfits.filter(favorite=False)

    style_stats = (
        ClothingItem.objects
        .filter(profile=profile)
        .values('predicted_style')
        .annotate(count=Count('predicted_style'))
        .order_by('-count')
    )

    total_styles = sum(s['count'] for s in style_stats)
    for s in style_stats:
        s['percent'] = round((s['count'] / total_styles) * 100)

    chart_labels = [s['predicted_style'].title() for s in style_stats]
    chart_data = [s['count'] for s in style_stats]

    return render(request, 'profile.html', {
        'form': form,
        'outfit_form': outfit_form,
        'profile': profile,
        'favorites': favorites,
        'non_favorites': non_favorites,
        'style_stats': style_stats,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })


# def wardrobe(request):
#     if request.method == 'POST':
#         form = ClothingItemForm(request.POST, request.FILES)
#         if form.is_valid():
#             item = form.save(commit=False)
#             item.profile = request.user.profile
#
#             # Description (BLIP)
#             description = describe_outfit(request.FILES['image'])
#             item.description = description
#
#             # Style (SentenceTransformer)
#             style = classify_style_from_text(description)
#             item.predicted_style = style
#
#             # Object Detection (YOLO)
#             image = Image.open(request.FILES['image']).convert("RGB")
#             labels = detect_clothing_objects(image)
#             print("DETECTED LABELS:", labels)
#             item.detected_labels = ', '.join(labels) if labels else 'None'
#
#             # Fine Category
#             label_map = categorize_from_labels(labels)
#             categories = [key for key, val in label_map.items() if val]
#             item.fine_category = ", ".join(categories) if categories else "Unknown"
#
#             if not categories:
#                 # 🟡 Fallback: use BLIP caption for category
#                 categories = [categorize_from_caption(description)]
#
#             item.fine_category = ", ".join(categories) if categories else "Unknown"
#
#             # Save clothing item
#             item.save()
#             return redirect('wardrobe')
#     else:
#         form = ClothingItemForm()
#
#     items = ClothingItem.objects.filter(profile=request.user.profile)
#     return render(request, 'wardrobe.html', {'form': form, 'items': items})

def wardrobe(request):
    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.profile = request.user.profile

            # Description (BLIP)
            description = describe_outfit(request.FILES['image'])
            item.description = description

            # Style (SentenceTransformer)
            style = classify_style_from_text(description)
            item.predicted_style = style

            # Object Detection (YOLO)
            image = Image.open(request.FILES['image']).convert("RGB")
            labels = detect_clothing_objects(image)
            print("DETECTED LABELS:", labels)
            item.detected_labels = ', '.join(labels) if labels else 'None'

            # Fine Category from YOLO
            label_map = categorize_from_labels(labels)
            categories = [key for key, val in label_map.items() if val]

            # Fallback to BLIP caption if YOLO failed
            if not categories:
                fallback = categorize_from_caption(description)
                categories = [fallback] if fallback else ["Unknown"]

            item.fine_category = ", ".join(categories)

            # Save clothing item
            item.save()
            return redirect('wardrobe')
    else:
        form = ClothingItemForm()

    items = ClothingItem.objects.filter(profile=request.user.profile)
    return render(request, 'wardrobe.html', {'form': form, 'items': items})

@login_required
def suggest_outfit(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return render(request, "suggest_outfit.html", {
            "outfit_combos": [],
            "message": "Please enter a style to generate outfit suggestions."
        })

    query_emb = embed(query)
    wardrobe = request.user.profile.clothes.all()

    if not wardrobe:
        return render(request, "suggest_outfit.html", {
            "outfit_combos": [],
            "message": "No clothing items found in your wardrobe."
        })

    grouped = group_by_category(wardrobe)
    combos = []

    # Combo: dress + accessories
    for dress in grouped["dress"]:
        for acc_combo in powerset(grouped["accessories"], max_len=2):
            combo = [dress] + list(acc_combo)
            desc = " ".join(f"{i.description} {i.predicted_style}" for i in combo)
            score = get_similarity(embed(desc), query_emb)
            combos.append((score, combo))

    # Combo: top + bottom (+ shoes) (+ accessories)
    for top in grouped["top"]:
        for bottom in grouped["bottom"]:
            for shoes in [None] + grouped["shoes"]:
                for acc_combo in powerset(grouped["accessories"], max_len=2):
                    combo = [top, bottom]
                    if shoes: combo.append(shoes)
                    combo.extend(acc_combo)
                    desc = " ".join(f"{i.description} {i.predicted_style}" for i in combo)
                    score = get_similarity(embed(desc), query_emb)
                    combos.append((score, combo))

    combos.sort(key=lambda x: x[0], reverse=True)
    combos = combos[:10]

    return render(request, "suggest_outfit.html", {
        "outfit_combos": combos,
        "query": query
    })

@login_required
def toggle_favorite(request, outfit_id):
    outfit = get_object_or_404(UserOutfit, id=outfit_id, profile=request.user.profile)
    outfit.favorite = not outfit.favorite
    outfit.save()
    return redirect('profile')

@login_required
def delete_outfit(request, outfit_id):
    outfit = get_object_or_404(UserOutfit, id=outfit_id, profile=request.user.profile)
    outfit.delete()
    return redirect('profile')

@login_required
def delete_clothing(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id, profile=request.user.profile)
    item.delete()
    return redirect('wardrobe')
