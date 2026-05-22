# Image Setup Guide for Mysore Unseen

This guide explains how to fetch and add proper images to the Artisan Explore and Food Discovery sections.

## Quick Start

Run this single command to fetch all images from Google and update the database:

```bash
python update_images_from_google.py
```

This will:
1. Fetch images from Google for all artisans
2. Fetch images from Google for all food establishments
3. Fetch images from Google for all artisan products
4. Fetch images from Google for all hidden gems
5. Fetch images from Google for all market stalls
6. Save them locally in `static/images/`
7. Update the database with image URLs

## What Gets Updated

### Artisan Explore Section
- **KSIC Silk Weavers** - Royal silk weaving heritage
- **Sri Krishna Murthy & Team** - Rosewood inlay artisans
- **Raghupathi Bhat** - Ganjifa card painting master
- **Mysore Sandalwood Carvers Guild** - Sandalwood sculpture specialists
- **B.S. Yogiraj Shilpi** - Traditional sculptor
- **Ramu Agarbathi Rollers** - Hand-rolled incense makers

### Food Discovery Section (18 establishments)
- **Tegu Mess** - Traditional home kitchen
- **Brahmin's Soda Factory** - Vintage refreshments
- **Anima Bhavan** - Traditional banana leaf meals
- **Poojari's Fish Land** - Mangalorean seafood
- **Sri Durga Bhavan** - Authentic South Indian idlis
- **Bonda Mane** - Evening snacks specialist
- **Mahadeshwara Butter Dosa** - Crispy dosas
- **Depth N Green** - Healthy cafe
- **Malgudi Cafe** - Heritage women-run cafe
- **Mahesh Prasad** - Popular local eatery
- **Sapa Bakery & Cafe** - Artisanal bakery
- **The Old House** - Heritage cafe with wood-fired pizza
- **Hotel RRR** - Legendary Andhra meals
- **Amruth Gobi Centre** - Street food specialist
- **Lakshman Mess** - Naati-style non-vegetarian
- **Usman Dry Gobi** - Cauliflower street food
- **Raju's Kadai** - Indo-Chinese street food
- **Lakshmi Tea Stall** - Roadside chai and snacks

## How It Works

1. **Google Images Search**: The script searches Google Images for each item with relevant keywords (name + category + location)
2. **Image Download**: Downloads the first valid image from search results
3. **Local Storage**: Saves images to `static/images/` with safe filenames
4. **Database Update**: Updates the database with `/static/images/filename.jpg` URLs and credits Google Images

## Image Display

Images are automatically displayed in the web interface:

- **Artisans Page** (`/artisans`): Shows artisan profile image
- **Artisan Detail** (`/artisans/<id>`): Shows profile image and products with images
- **Food Discovery** (`/food-discovery`): Shows food establishment images in the grid
- **Marketplace** (`/marketplace`): Shows product images
- **Hidden Gems** (`/hidden-gems`): Shows location images
- **Explore** (`/explore`): Shows category images with filtering

## Manual Execution

If the automated script fails, you can also manually update specific sections:

```bash
# Just artisans
python update_images_from_google.py

# Then run app
python app.py
```

## Troubleshooting

### Images not downloading?
- Check your internet connection
- Verify `static/images/` directory exists
- Try increasing the `time.sleep()` delay between requests to avoid rate limiting
- Some images may fail if Google Images blocks the request

### Images not showing in browser?
1. Check browser console for 404 errors
2. Verify image files exist in `static/images/`
3. Refresh the page with Ctrl+Shift+R (hard refresh)
4. Check that Flask is serving static files (it does by default)

### Database not updating?
1. Ensure the database file exists: `mysore_unseen.db`
2. Check that you have write permissions in the directory
3. Run `python seed_data.py` first if starting fresh
4. Check the console output for error messages

## File Structure

```
mysore-unseen/
├── app.py                      # Flask application
├── models.py                   # Database models
├── seed_data.py               # Initial data seeding
├── update_images_from_google.py   # ← Run this to fetch images
├── mysore_unseen.db           # SQLite database
├── static/
│   ├── images/
│   │   ├── KSIC_Silk_Weavers.jpg
│   │   ├── Sri_Krishna_Murthy___Team.jpg
│   │   ├── Tegu_Mess.jpg
│   │   ├── Brahmin_s_Soda_Factory.jpg
│   │   └── ... (all fetched images)
│   ├── style.css
│   └── script.js
└── templates/
    ├── artisans.html          # Displays artisan images
    ├── food_discovery.html    # Displays food images
    └── ...
```

## Image Credits

All images are fetched from Google Images and credited as "Google Images" in the database. Users should verify fair use and copyright when displaying these images publicly.

## Performance Notes

- First run may take 10-15 minutes (18+ API calls with 1.5s delays)
- Subsequent runs are faster as they skip existing images
- Images are cached locally, so no repeated downloads

## Next Steps

1. Run: `python update_images_from_google.py`
2. Start the app: `python app.py`
3. Open: `http://localhost:5000`
4. Visit `/artisans` and `/food-discovery` to see the images
