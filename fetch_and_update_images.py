import json
from pathlib import Path

import requests

from image_data import PLACE_IMAGES as CURRENT_PLACE_IMAGES, ARTISAN_IMAGES as CURRENT_ARTISAN_IMAGES, FOOD_IMAGES as CURRENT_FOOD_IMAGES

WIKIPEDIA_QUERIES = [
    # Hidden gems and places
    ("Shuka Vana (Parrot Park)", "PLACE", "Shuka Vana (Parrot Park)"),
    ("Lingambudhi Lake", "PLACE", "Lingambudhi Lake"),
    ("Kukkarahalli Lake", "PLACE", "Kukkarahalli Lake"),
    ("Karanji Lake", "PLACE", "Karanji Lake"),
    ("Jayalakshmi Vilas Mansion", "PLACE", "Jayalakshmi Vilas Mansion Folklore Museum"),
    ("Melody World Wax Museum", "PLACE", "Melody World Wax Museum"),
    ("Mysore Zoo", "PLACE", "Mysore Zoo"),
    ("St. Philomena's Church, Mysore", "PLACE", "St. Philomena's Church"),
    ("Chamundeshwari Temple", "PLACE", "Chamundeshwari Temple"),
    ("Chamundi Hills", "PLACE", "Chamundi Hills"),
    ("Devaraja Market", "PLACE", "Devaraja Market"),
    ("Brindavan Gardens", "PLACE", "Brindavan Gardens"),
    ("Railway Museum, Mysore", "PLACE", "Railway Museum"),
    ("Jaganmohan Palace", "PLACE", "Jaganmohan Palace"),
    ("Tippu Sultan's Summer Palace", "PLACE", "Tippu Sultan's Summer Palace"),
    ("Karanji Lake Butterfly Park", "PLACE", "Karanji Lake Butterfly Park"),
    ("Gopalakrishna Adiga", "PLACE", "Gopalakrishna Adiga's House"),
    ("Srirangapatna Gumbaz", "PLACE", "Srirangapatna Gumbaz"),
    ("Chunchanakatte Falls", "PLACE", "Chunchanakatte Falls"),
    ("Bhogadi Lake", "PLACE", "Bhogadi Lake"),
    ("Old Palace Elephant Stables", "PLACE", "Old Palace Elephant Stables"),
    ("Sri Nandi Temple", "PLACE", "Sri Nandi Temple (Monolithic Bull)"),
    ("Varuna Lake", "PLACE", "Varuna Lake"),
    ("Guru Sweet Mart", "PLACE", "Mysore Pak"),
    ("Tonachi Village Weavers", "PLACE", "Mysore silk"),
    ("Sri Krishna Murthy Inlay Arts", "PLACE", "Rosewood inlay"),
    ("Raghupathi Bhat Ganjifa Studio", "PLACE", "Ganjifa"),
    ("Sand Sculpture Museum", "PLACE", "Sand Sculpture Museum"),
    ("Mysore Palace", "PLACE", "Mysore Palace"),
    ("Cauvery", "PLACE", "Kaveri River"),
    ("Cauvery Karnataka State Arts & Crafts Emporium", "PLACE", "Karnataka State Handicrafts Development Corporation"),
    ("Mysore Sand Sculpture Museum", "PLACE", "Sand Sculpture Museum"),
    ("Mysore Zoo (Sri Chamarajendra Zoological Gardens)", "PLACE", "Mysore Zoo"),
    # Artisans and crafts
    ("Mysore silk", "ARTISAN", "KSIC Silk Weavers"),
    ("Rosewood inlay", "ARTISAN", "Sri Krishna Murthy"),
    ("Ganjifa", "ARTISAN", "Raghupathi Bhat"),
    ("Sandalwood carving", "ARTISAN", "Mysore Sandalwood Carvers Guild"),
    ("Sculpture", "ARTISAN", "B.S. Yogiraj Shilpi"),
    ("Incense", "ARTISAN", "Ramu Agarbathi Rollers"),
    # Food and drink
    ("Bonda (Indian snack)", "FOOD", "Aloo Bonda"),
    ("Sourdough", "FOOD", "Artisanal Sourdough"),
    ("Dosa", "FOOD", "Benne Masala Dosa"),
    ("Dosa", "FOOD", "Butter Dosa"),
    ("Bhelpuri", "FOOD", "Churmuri"),
    ("Dosa", "FOOD", "Dosa"),
    ("Gobi Manchurian", "FOOD", "Dry Gobi"),
    ("Indian filter coffee", "FOOD", "Filter Coffee"),
    ("Idli", "FOOD", "Idli"),
    ("Idli vada", "FOOD", "Idli Vada"),
    ("Mangalorean cuisine", "FOOD", "Mangalorean Fish Curry"),
    ("Masala dosa", "FOOD", "Masala Dosa"),
    ("Hamburger", "FOOD", "Millet Burgers"),
    ("Biryani", "FOOD", "Mutton Biryani"),
    ("Masala dosa", "FOOD", "Mysore Masala Dosa"),
    ("Mysore Pak", "FOOD", "Mysore Pak"),
    ("Ragi mudde", "FOOD", "Ragi Mudde"),
    ("Sarsaparilla", "FOOD", "Sarsaparilla Soda"),
    ("Thali", "FOOD", "South Indian Thali"),
    ("Idli", "FOOD", "Thatte Idli"),
    ("Pizza", "FOOD", "Wood-fired Pizza"),
]

FALLBACK_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Mysore_Palace_Morning.jpg/800px-Mysore_Palace_Morning.jpg"
WIKI_API_URL = "https://en.wikipedia.org/w/api.php"


def fetch_wikipedia_thumbnail(title: str) -> str:
    params = {
        "action": "query",
        "prop": "pageimages",
        "pithumbsize": "800",
        "format": "json",
        "titles": title,
    }
    try:
        response = requests.get(
            WIKI_API_URL,
            params=params,
            timeout=15,
            headers={"User-Agent": "MysoreUnseenImageFetcher/1.0 (https://example.com)"},
        )
        response.raise_for_status()
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        if not pages:
            return FALLBACK_IMAGE
        page = next(iter(pages.values()))
        thumbnail = page.get("thumbnail", {}).get("source")
        if thumbnail:
            return thumbnail
    except Exception as exc:
        print(f"[ERROR] Failed to fetch '{title}': {exc}")
    return FALLBACK_IMAGE


def search_wikipedia_title(search_term: str) -> str | None:
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "srlimit": "1",
        "format": "json",
    }
    try:
        response = requests.get(
            WIKI_API_URL,
            params=params,
            timeout=15,
            headers={"User-Agent": "MysoreUnseenImageFetcher/1.0 (https://example.com)"},
        )
        response.raise_for_status()
        data = response.json()
        hits = data.get("query", {}).get("search", [])
        if hits:
            return hits[0].get("title")
    except Exception as exc:
        print(f"[ERROR] Wikipedia search failed for '{search_term}': {exc}")
    return None


def fetch_thumbnail_with_fallback(title: str) -> str:
    image_url = fetch_wikipedia_thumbnail(title)
    if image_url != FALLBACK_IMAGE:
        return image_url
    search_title = search_wikipedia_title(title)
    if search_title:
        print(f"[INFO] Searching for '{title}' found '{search_title}'")
        image_url = fetch_wikipedia_thumbnail(search_title)
        if image_url != FALLBACK_IMAGE:
            return image_url
    return FALLBACK_IMAGE


def format_mapping(mapping: dict, name: str) -> str:
    items = []
    for key in sorted(mapping.keys(), key=lambda s: s.lower()):
        items.append(f'    {json.dumps(key)}: {json.dumps(mapping[key])},')
    return f"{name} = {{\n" + "\n".join(items) + "\n}\n"


def main() -> None:
    place_images = dict(CURRENT_PLACE_IMAGES)
    artisan_images = dict(CURRENT_ARTISAN_IMAGES)
    food_images = dict(CURRENT_FOOD_IMAGES)

    print("Fetching Wikipedia thumbnails...")
    for title, category, key in WIKIPEDIA_QUERIES:
        image_url = fetch_thumbnail_with_fallback(title)
        print(f"{title} -> {key}: {image_url}")
        if image_url == FALLBACK_IMAGE:
            print(f"[SKIP] Keeping existing image for '{key}' because no valid Wikipedia thumbnail was found.")
            continue
        if category == "PLACE":
            place_images[key] = image_url
            if key == "Shuka Vana (Parrot Park)":
                place_images["Shuka Vana"] = image_url
        elif category == "ARTISAN":
            artisan_images[key] = image_url
        elif category == "FOOD":
            food_images[key] = image_url

    file_path = Path(__file__).with_name("image_data.py")
    output = [
        "# image_data.py - Verified Wikipedia thumbnail URLs for Mysore Unseen",
        "",
        format_mapping(place_images, "PLACE_IMAGES"),
        "",
        format_mapping(artisan_images, "ARTISAN_IMAGES"),
        "",
        format_mapping(food_images, "FOOD_IMAGES"),
        "",
        f'DEFAULT_IMAGE = {json.dumps(FALLBACK_IMAGE)}',
        "",
        "def get_image(mapping, name):",
        "    if not name:",
        "        return DEFAULT_IMAGE",
        "    name_lower = name.lower()",
        "    for key, url in mapping.items():",
        "        if key.lower() in name_lower or name_lower in key.lower():",
        "            return url",
        "    return DEFAULT_IMAGE",
        "",
    ]

    file_text = "\n".join(output)
    file_path.write_text(file_text, encoding="utf-8")
    print(f"\nWrote updated image_data.py to {file_path}")


if __name__ == "__main__":
    main()
