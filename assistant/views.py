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
from django.db.models import Count, Max
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
from django.db.models import Count, Max

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

# @login_required
# def profile(request):
#     profile = request.user.profile
#
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         outfit_form = UserOutfitForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             profile = form.save()
#             if profile.profile_picture:
#                 image_path = profile.profile_picture.path
#                 description = describe_outfit(image_path)
#                 style = classify_style_from_text(description)
#                 profile.predicted_style = f"{description} ⟶ {style}"
#                 profile.save()
#             return redirect('profile')
#
#         if outfit_form.is_valid():
#             outfit = outfit_form.save(commit=False)
#             outfit.profile = profile
#
#             description = describe_outfit(outfit.image)
#             style = classify_style_from_text(description)
#             outfit.description = description
#             outfit.predicted_style = style
#
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
#         form = ProfileForm(instance=profile)
#         outfit_form = UserOutfitForm()
#
#     outfits = profile.user_outfits.all()
#     top_rating = outfits.aggregate(max_rating=Max('rating'))['max_rating']
#     top_rated_outfits = outfits.filter(rating=top_rating) if top_rating else []
#     favorites_count = outfits.filter(favorite=True).count()
#
#     style_stats = (
#         ClothingItem.objects
#         .filter(profile=profile)
#         .values('predicted_style')
#         .annotate(count=Count('predicted_style'))
#         .order_by('-count')
#     )
#
#     total_styles = sum(s['count'] for s in style_stats)
#     for s in style_stats:
#         s['percent'] = round((s['count'] / total_styles) * 100)
#
#     chart_labels = [s['predicted_style'].title() for s in style_stats]
#     chart_data = [s['count'] for s in style_stats]
#
#     return render(request, 'profile.html', {
#         'form': form,
#         'outfit_form': outfit_form,
#         'profile': profile,
#         'outfits': outfits,
#         'style_stats': style_stats,
#         'chart_labels': chart_labels,
#         'chart_data': chart_data,
#         'top_rated_outfits': top_rated_outfits,
#         'favorites_count': favorites_count,
#     })

from django.db.models import Count, Max
# ...

# @login_required
# def profile(request):
#     profile = request.user.profile
#
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         outfit_form = UserOutfitForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             profile = form.save()
#             if profile.profile_picture:
#                 image_path = profile.profile_picture.path
#                 description = describe_outfit(image_path)
#                 style = classify_style_from_text(description)
#                 profile.predicted_style = f"{description} ⟶ {style}"
#                 profile.save()
#             return redirect('profile')
#
#         if outfit_form.is_valid():
#             outfit = outfit_form.save(commit=False)
#             outfit.profile = profile
#
#             description = describe_outfit(outfit.image)
#             style = classify_style_from_text(description)
#             outfit.description = description
#             outfit.predicted_style = style
#
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
#         form = ProfileForm(instance=profile)
#         outfit_form = UserOutfitForm()
#
#     outfits = profile.user_outfits.all()
#
#     # --- КАЖУВАЧИ ЗА HEADER ---
#     outfits_count   = outfits.count()
#     styles_count    = outfits.values('predicted_style').distinct().count()
#     favorites_count = outfits.filter(favorite=True).count()
#
#     # Top rated
#     top_rating = outfits.aggregate(max_rating=Max('rating'))['max_rating']
#     top_rated_outfits = outfits.filter(rating=top_rating) if top_rating else []
#
#     # Chart (си останува за ClothingItem)
#     style_stats = (
#         ClothingItem.objects
#         .filter(profile=profile)
#         .values('predicted_style')
#         .annotate(count=Count('predicted_style'))
#         .order_by('-count')
#     )
#     total_styles = sum(s['count'] for s in style_stats) or 1
#     for s in style_stats:
#         s['percent'] = round((s['count'] / total_styles) * 100)
#
#     chart_labels = [s['predicted_style'].title() for s in style_stats]
#     chart_data   = [s['count'] for s in style_stats]
#
#     return render(request, 'profile.html', {
#         'form': form,
#         'outfit_form': outfit_form,
#         'profile': profile,
#         'outfits': outfits,
#         'outfits_count': outfits_count,     # NEW
#         'styles_count': styles_count,       # NEW
#         'favorites_count': favorites_count, # EXISTS
#         'style_stats': style_stats,
#         'chart_labels': chart_labels,
#         'chart_data': chart_data,
#         'top_rated_outfits': top_rated_outfits,
#     })


# ->>>>>>>HEREEEEEEEE
# @login_required
# def profile(request):
#     profile = request.user.profile
#
#     if request.method == 'POST':
#         kind = request.POST.get('form_kind')
#
#         # === Аватар/профил форма ===
#         if kind == 'avatar':
#             form = ProfileForm(request.POST, request.FILES, instance=profile)
#             outfit_form = UserOutfitForm()  # празна за да ја прикажеме пак
#             if form.is_valid():
#                 profile = form.save()
#                 if profile.profile_picture:
#                     image_path = profile.profile_picture.path
#                     description = describe_outfit(image_path)
#                     style = classify_style_from_text(description)
#                     profile.predicted_style = f"{description} ⟶ {style}"
#                     profile.save()
#                 return redirect('profile')
#
#         # === Add Outfit форма ===
#         elif kind == 'outfit':
#             form = ProfileForm(instance=profile)  # празна профил форма
#             outfit_form = UserOutfitForm(request.POST, request.FILES)
#             if outfit_form.is_valid():
#                 outfit = outfit_form.save(commit=False)
#                 outfit.profile = profile
#
#                 # Caption + Style
#                 description = describe_outfit(outfit.image)
#                 style = classify_style_from_text(description)
#                 outfit.description = description
#                 outfit.predicted_style = style
#
#                 # Детекција/категории
#                 img = Image.open(outfit.image).convert("RGB")
#                 labels = detect_clothing_objects(img)
#                 outfit.detected_labels = ', '.join(labels) if labels else 'None'
#
#                 label_map = categorize_from_labels(labels)
#                 categories = [k for k, v in label_map.items() if v]
#                 outfit.fine_category = ", ".join(categories) if categories else "Unknown"
#
#                 outfit.save()
#                 return redirect('profile')
#
#         # fallback ако нема form_kind
#         else:
#             form = ProfileForm(instance=profile)
#             outfit_form = UserOutfitForm()
#     else:
#         form = ProfileForm(instance=profile)
#         outfit_form = UserOutfitForm()
#
#     outfits = profile.user_outfits.all()
#
#     outfits_count   = outfits.count()
#     styles_count    = outfits.values('predicted_style').distinct().count()
#     favorites_count = outfits.filter(favorite=True).count()
#
#     top_rating = outfits.aggregate(max_rating=Max('rating'))['max_rating']
#     top_rated_outfits = outfits.filter(rating=top_rating) if top_rating else []
#
#     style_stats = (
#         ClothingItem.objects
#         .filter(profile=profile)
#         .values('predicted_style')
#         .annotate(count=Count('predicted_style'))
#         .order_by('-count')
#     )
#     total_styles = sum(s['count'] for s in style_stats) or 1
#     for s in style_stats:
#         s['percent'] = round((s['count'] / total_styles) * 100)
#
#     chart_labels = [s['predicted_style'].title() for s in style_stats]
#     chart_data   = [s['count'] for s in style_stats]
#
#     return render(request, 'profile.html', {
#         'form': form,
#         'outfit_form': outfit_form,
#         'profile': profile,
#         'outfits': outfits,
#         'outfits_count': outfits_count,
#         'styles_count': styles_count,
#         'favorites_count': favorites_count,
#         'style_stats': style_stats,
#         'chart_labels': chart_labels,
#         'chart_data': chart_data,
#         'top_rated_outfits': top_rated_outfits,
#     })
#

# ->>>>>> HEREEEEEE

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


# -c
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
#             # Fine Category from YOLO
#             label_map = categorize_from_labels(labels)
#             categories = [key for key, val in label_map.items() if val]
#
#             # Fallback to BLIP caption if YOLO failed
#             if not categories:
#                 fallback = categorize_from_caption(description)
#                 categories = [fallback] if fallback else ["Unknown"]
#
#             item.fine_category = ", ".join(categories)
#
#             # Save clothing item
#             item.save()
#             return redirect('wardrobe')
#     else:
#         form = ClothingItemForm()
#
#     items = ClothingItem.objects.filter(profile=request.user.profile)
#     return render(request, 'wardrobe.html', {'form': form, 'items': items})
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
# def toggle_favorite(request, outfit_id):
#     outfit = get_object_or_404(UserOutfit, id=outfit_id, profile=request.user.profile)
#     outfit.favorite = not outfit.favorite
#     outfit.save()
#     return redirect('profile')
#
# @login_required
# def delete_outfit(request, outfit_id):
#     outfit = get_object_or_404(UserOutfit, id=outfit_id, profile=request.user.profile)
#     outfit.delete()
#     return redirect('profile')
#
# @login_required
# def delete_clothing(request, item_id):
#     item = get_object_or_404(ClothingItem, id=item_id, profile=request.user.profile)
#     item.delete()
#     return redirect('wardrobe')


# ------->>>>>> HEREEE



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max
from itertools import product
from PIL import Image
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date, parse_datetime


from .forms import UserRegisterForm, ProfileForm, ClothingItemForm, UserOutfitForm,OutfitPlanForm
from .models import ClothingItem, UserOutfit, OutfitPlan

# bring everything you already expose from fashion_model
from .fashion_model import (
    describe_outfit, classify_style_from_text,
    detect_clothing_objects, embed, get_similarity,
    categorize_from_labels, group_by_category, powerset, categorize_from_caption,
    # NEW:
    predict_style
)

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
        kind = request.POST.get('form_kind')

        # === Avatar/Profile form ===
        if kind == 'avatar':
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            outfit_form = UserOutfitForm()
            if form.is_valid():
                profile = form.save()
                if profile.profile_picture:
                    image_path = profile.profile_picture.path
                    description = describe_outfit(image_path)
                    # keep your original "predicted_style" text for the profile picture
                    style = classify_style_from_text(description)
                    profile.predicted_style = f"{description} ⟶ {style}"
                    profile.save()
                return redirect('profile')

        # === Add Outfit form ===
        elif kind == 'outfit':
            form = ProfileForm(instance=profile)
            outfit_form = UserOutfitForm(request.POST, request.FILES)
            if outfit_form.is_valid():
                outfit = outfit_form.save(commit=False)
                outfit.profile = profile

                # Caption
                description = describe_outfit(outfit.image)
                outfit.description = description

                # YOLO + labels (stored)
                img = Image.open(outfit.image).convert("RGB")
                labels = detect_clothing_objects(img)
                outfit.detected_labels = ', '.join(labels) if labels else 'None'

                # Fine categories from YOLO + fallback to BLIP caption
                label_map = categorize_from_labels(labels)
                categories = [k for k, v in label_map.items() if v]
                if not categories:
                    fallback = categorize_from_caption(description)
                    categories = [fallback] if fallback else ["Unknown"]
                outfit.fine_category = ", ".join(categories)

                # NEW: CLIP-based style prediction (robust)
                style = predict_style(img, description, labels)
                outfit.predicted_style = style

                outfit.save()
                return redirect('profile')

        else:
            form = ProfileForm(instance=profile)
            outfit_form = UserOutfitForm()
    else:
        form = ProfileForm(instance=profile)
        outfit_form = UserOutfitForm()

    outfits = profile.user_outfits.all()
    outfits_count   = outfits.count()
    styles_count    = outfits.values('predicted_style').distinct().count()
    favorites_count = outfits.filter(favorite=True).count()

    top_rating = outfits.aggregate(max_rating=Max('rating'))['max_rating']
    top_rated_outfits = outfits.filter(rating=top_rating) if top_rating else []

    # Chart is computed from ClothingItem (kept)
    style_stats = (
        ClothingItem.objects
        .filter(profile=profile)
        .values('predicted_style')
        .annotate(count=Count('predicted_style'))
        .order_by('-count')
    )
    total_styles = sum(s['count'] for s in style_stats) or 1
    for s in style_stats:
        s['percent'] = round((s['count'] / total_styles) * 100)

    chart_labels = [s['predicted_style'].title() for s in style_stats]
    chart_data   = [s['count'] for s in style_stats]

    return render(request, 'profile.html', {
        'form': form,
        'outfit_form': outfit_form,
        'profile': profile,
        'outfits': outfits,
        'outfits_count': outfits_count,
        'styles_count': styles_count,
        'favorites_count': favorites_count,
        'style_stats': style_stats,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'top_rated_outfits': top_rated_outfits,
    })

@login_required
def wardrobe(request):
    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.profile = request.user.profile

            # BLIP description
            description = describe_outfit(request.FILES['image'])
            item.description = description

            # YOLO detection
            image = Image.open(request.FILES['image']).convert("RGB")
            labels = detect_clothing_objects(image)
            print("DETECTED LABELS:", labels)
            item.detected_labels = ', '.join(labels) if labels else 'None'

            # Fine category from YOLO (fallback to BLIP if empty)
            label_map = categorize_from_labels(labels)
            categories = [key for key, val in label_map.items() if val]
            if not categories:
                fallback = categorize_from_caption(description)
                categories = [fallback] if fallback else ["Unknown"]
            item.fine_category = ", ".join(categories)

            # NEW: CLIP-based style prediction for wardrobe items too
            item.predicted_style = predict_style(image, description, labels)

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

    # dress + accessories
    for dress in grouped["dress"]:
        for acc_combo in powerset(grouped["accessories"], max_len=2):
            combo = [dress] + list(acc_combo)
            desc = " ".join(f"{i.description} {i.predicted_style}" for i in combo)
            score = get_similarity(embed(desc), query_emb)
            combos.append((score, combo))

    # top + bottom (+ shoes) (+ accessories)
    for top in grouped["top"]:
        for bottom in grouped["bottom"]:
            for shoes in [None] + grouped["shoes"]:
                for acc_combo in powerset(grouped["accessories"], max_len=2):
                    combo = [top, bottom]
                    if shoes:
                        combo.append(shoes)
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

@login_required
def calendar_view(request):
    """Рендер страница со календар + dropdown за избор на outfit."""
    outfits = request.user.profile.user_outfits.all().order_by('-rating', '-id')
    form = OutfitPlanForm()
    return render(request, 'calendar.html', {'form': form, 'outfits': outfits})

@require_GET
@login_required
def calendar_events(request):
    profile = request.user.profile
    start = request.GET.get('start')
    end   = request.GET.get('end')

    def to_date(s: str | None):
        if not s:
            return None
        # 1) ако е само YYYY-MM-DD
        d = parse_date(s)
        if d:
            return d
        # 2) ако е ISO со време/зона -> земи .date()
        dt = parse_datetime(s)
        return dt.date() if dt else None

    sdate = to_date(start)
    edate = to_date(end)

    qs = OutfitPlan.objects.filter(profile=profile)
    if sdate:
        qs = qs.filter(date__gte=sdate)
    if edate:
        qs = qs.filter(date__lte=edate)

    events = []
    for p in qs.select_related('outfit'):
        events.append({
            "id": p.id,
            "title": f"{p.outfit.predicted_style} ⭐{p.outfit.rating}",
            "start": p.date.isoformat(),
            "allDay": True,
            "extendedProps": {
                "image": p.outfit.image.url,
                "style": p.outfit.predicted_style,
                "note": p.note or "",
                "outfitId": p.outfit_id,
            }
        })
    return JsonResponse(events, safe=False)


@require_POST
@login_required
def calendar_add(request):
    profile = request.user.profile
    outfit_id = request.POST.get('outfit')
    date_str  = request.POST.get('date')
    note      = request.POST.get('note', '').strip()

    if not (outfit_id and date_str):
        return HttpResponseBadRequest("Missing outfit or date.")

    outfit = get_object_or_404(UserOutfit, id=outfit_id, profile=profile)
    date = parse_date(date_str)
    if not date:
        return HttpResponseBadRequest("Bad date.")

    plan, _created = OutfitPlan.objects.get_or_create(profile=profile, outfit=outfit, date=date, defaults={"note": note})
    if not _created and note:
        plan.note = note
        plan.save()

    return JsonResponse({"ok": True, "id": plan.id})

@require_POST
@login_required
def calendar_delete(request, plan_id):
    profile = request.user.profile
    plan = get_object_or_404(OutfitPlan, id=plan_id, profile=profile)
    plan.delete()
    return JsonResponse({"ok": True})



