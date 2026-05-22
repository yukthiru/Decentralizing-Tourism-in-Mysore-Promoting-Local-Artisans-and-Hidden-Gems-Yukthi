# Image Fetching Scripts - Complete Guide

This document explains all the image-related scripts in the project and when to use each one.

## Overview Scripts

### 1. **update_images_from_google.py** ⭐ (RECOMMENDED)
**Purpose**: Fetch proper Google Images for artisans, food, products, gems, and stalls, then update the database.

**When to use**: 
- When you want to add real images to artisans and food discovery
- After seeding the database with `seed_data.py`

**Usage**:
```bash
python update_images_from_google.py
```

**What it does**:
- Searches Google Images for each artisan with query: "{Name} {Craft} artisan Mysore"
- Searches Google Images for each food place with query: "{Name} {Type} Mysore food"
- Downloads images to `static/images/`
- Updates database records with image URLs (`/static/images/filename.jpg`)
- Adds 1.5 second delay between requests to avoid rate limiting

**Output**: 
- 50+ JPG images in `static/images/`
- Updated database with image URLs for:
  - 6 Artisans
  - 18 Food establishments
  - 14 Artisan products
  - 13 Hidden gems
  - 6 Market stalls
  - 4 Local guides
  - 6 Stay options

**Time**: ~15-20 minutes (due to intentional 1.5s delays)

---

### 2. **fetch_images_comprehensive.py**
**Purpose**: Advanced image fetcher with granular control and error handling

**When to use**: 
- If you need finer control over which items get images
- For debugging or retrying failed downloads
- If you want to overwrite existing images

**Usage**:
```bash
# Fetch all types of images
python fetch_images_comprehensive.py

# Fetch only artisans
python fetch_images_comprehensive.py --target artisans

# Fetch only food
python fetch_images_comprehensive.py --target food

# Fetch products only
python fetch_images_comprehensive.py --target products

# Fetch gems only
python fetch_images_comprehensive.py --target gems

# Fetch stalls only
python fetch_images_comprehensive.py --target stalls

# Overwrite existing images
python fetch_images_comprehensive.py --overwrite
```

**Advantages over basic script**:
- More detailed output and logging
- Per-category fetching
- Can overwrite existing images
- Better error handling and recovery

---

### 3. **fetch_images_google.py**
**Purpose**: Legacy Google image fetcher (original version)

**When to use**: 
- Only if you need the original implementation
- For bulk fetching all place names from seed_data.py

**Usage**:
```bash
# Fetch images for all seeded items
python fetch_images_google.py

# Limit to first N items
python fetch_images_google.py --limit 10

# Overwrite existing images
python fetch_images_google.py --overwrite
```

---

### 4. **Other Legacy Scripts**

#### fetch_and_update_images.py
- Updates database with local images
- Use if you already have images downloaded locally

#### fetch_hidden_images.py
- Specifically for hidden gems
- Useful if you only want to update gems

#### duckduckgo_image_fetch.py
- Uses DuckDuckGo instead of Google
- Alternative when Google Images is blocked

#### fetch_specific_bing_images.py, bing_image_search.py
- Use Bing Image Search instead of Google
- Backup option if Google not available

---

## Typical Workflow

### Fresh Setup (Start from scratch)

```bash
# Step 1: Seed the database with initial data
python seed_data.py

# Step 2: Fetch images from Google
python update_images_from_google.py

# Step 3: Start the application
python app.py

# Step 4: Visit http://localhost:5000
# Check /artisans and /food-discovery
```

### Updating Specific Items Only

```bash
# If you only added new artisans and want their images:
python fetch_images_comprehensive.py --target artisans

# If you only added new food establishments:
python fetch_images_comprehensive.py --target food
```

### Troubleshooting

```bash
# If images didn't download properly, retry with verbose output:
python fetch_images_comprehensive.py --overwrite

# If specific items failed, check the database:
# Run analyze_db.py to see which items have/don't have images
```

---

## Database Structure

### Artisan Table
```sql
SELECT id, name, craft, image_url FROM artisan;
```
- `image_url`: Path to artisan's profile image (e.g., `/static/images/KSIC_Silk_Weavers.jpg`)
- `image_credit`: Usually "Google Images"

### LocalFood Table
```sql
SELECT id, name, food_type, image_url FROM local_food;
```
- `image_url`: Path to food establishment's image
- `image_credit`: Usually "Google Images"

### ArtisanProduct Table
```sql
SELECT id, product_name, category, image_url FROM artisan_product;
```
- `image_url`: Path to product image

### HiddenGem Table
```sql
SELECT id, name, category, image_url FROM hidden_gem;
```
- `image_url`: Path to location/gem image

### MarketStall Table
```sql
SELECT id, stall_name, image_url FROM market_stall;
```
- `image_url`: Path to stall image

---

## Image Naming Convention

Images are named using the entity's name, converted to safe filenames:

```
Entity Name          → Filename
─────────────────────────────────────
KSIC Silk Weavers    → KSIC_Silk_Weavers.jpg
Sri Krishna Murthy   → Sri_Krishna_Murthy___Team.jpg
Tegu Mess            → Tegu_Mess.jpg
Brahmin's Soda       → Brahmin_s_Soda_Factory.jpg
```

Rules:
- Spaces become underscores
- Special characters become underscores
- All lowercase → Can be mixed case for readability
- Always .jpg extension

---

## Monitoring Progress

### Check Image Download Progress
```bash
# During script execution, watch the output:
# ✓ indicates successful downloads
# ✗ indicates failures
```

### Verify Images Locally
```bash
# List all downloaded images
dir static\images\*.jpg

# Count total images
dir static\images\*.jpg | measure
```

### Verify Database Updates
```bash
# Check if artisans have images
python -c "from app import app; from models import *; \
with app.app_context(): \
    print([a.image_url for a in Artisan.query.all()])"
```

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| No images download | Network issue | Check internet, try later |
| 404 errors in browser | Flask not serving static files | Ensure `static/` folder exists, restart Flask |
| Database not updating | Permission issue | Check write permissions in project directory |
| Slow downloads | Rate limiting | The 1.5s delay is intentional, don't reduce |
| Specific item missing image | Failed download | Run `--overwrite` flag to retry |

---

## Best Practices

1. **Always seed first**: Run `seed_data.py` before fetching images
2. **Use recommended script**: Use `update_images_from_google.py` for simplicity
3. **Don't interrupt**: Let the full script complete (15-20 mins)
4. **Check output**: Review console output for any ✗ failures
5. **Hard refresh browser**: Use Ctrl+Shift+R to clear browser cache

---

## Next Steps

After images are downloaded:

1. Test the application locally:
   ```bash
   python app.py
   ```

2. Visit the following pages to verify images:
   - http://localhost:5000/artisans (Artisan Explore)
   - http://localhost:5000/food-discovery (Food Discovery)
   - http://localhost:5000/marketplace (Products with images)
   - http://localhost:5000/hidden-gems (Location images)

3. If satisfied, deploy your application:
   ```bash
   # Ensure all images are in static/images/ directory
   # Deploy entire project including static/ folder
   gunicorn app:app
   ```

---

## Related Documentation

- `IMAGES_SETUP.md` - Quick start guide for image setup
- `README.md` - Main project documentation
- `models.py` - Database schema for image fields
- `seed_data.py` - Initial data with image URLs

