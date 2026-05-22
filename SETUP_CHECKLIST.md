# Image Setup Checklist ✓

Follow this checklist to add images to your Mysore Unseen application.

## Pre-Setup
- [ ] Ensure you have Python 3.6+ installed
- [ ] Ensure you have 500MB free disk space (for images)
- [ ] Ensure you have a stable internet connection
- [ ] CD into the project directory: `cd mysore-unseen`

## Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
- [ ] Command completed without errors
- [ ] Flask installed
- [ ] requests library installed
- [ ] flask-sqlalchemy installed

## Step 2: Initialize Database
```bash
python seed_data.py
```
- [ ] Command completed without errors
- [ ] Database file created: `mysore_unseen.db`
- [ ] Console shows "Database fully seeded with real Mysore data!"
- [ ] ~70+ items added to database

Expected output includes:
- ✓ "Dropping existing tables..."
- ✓ "Creating fresh tables..."
- ✓ "Seeding Obscure Hidden Gems & Locations..."
- ✓ "Seeding Real Artisans..."
- ✓ "Seeding Authentic Artisan Products..."
- ✓ "Seeding Obscure Local Food Discoveries..."
- ✓ "Database fully seeded..."

## Step 3: Fetch Images from Google
```bash
python update_images_from_google.py
```
- [ ] Command started
- [ ] Console shows download progress
- [ ] Images folder being populated: `static/images/`

Expected flow:
1. **Artisans section** - 6 images downloaded
2. **Food section** - 18 images downloaded
3. **Products section** - 14 images downloaded
4. **Hidden Gems section** - 13 images downloaded
5. **Market Stalls section** - 6 images downloaded
6. **All database records updated** with image URLs

Expected time: **15-20 minutes** (due to intentional 1.5s delays)

**Monitor the output for**:
- ✓ Markers = downloading
- ✓ Check marks = successful downloads
- ✗ X marks = failed downloads (will retry)
- ✓ Database updated messages

## Step 4: Verify Images Downloaded
```bash
# Check image count (Windows)
dir static\images\*.jpg | measure-object

# Or just list them
dir static\images\*.jpg

# Should show 50+ JPG files
```
- [ ] At least 50 JPG images in `static/images/`
- [ ] Images have names like: `KSIC_Silk_Weavers.jpg`, `Tegu_Mess.jpg`, etc.
- [ ] All files have reasonable size (> 5KB)

## Step 5: Start Application
```bash
python app.py
```
- [ ] Flask server starts successfully
- [ ] Console shows: "Running on http://127.0.0.1:5000"
- [ ] No error messages

Expected console output:
```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://127.0.0.1:5000
```

## Step 6: Verify Images Display

### Open Browser
- [ ] Open: http://localhost:5000/artisans
- [ ] Page loads successfully
- [ ] All 6 artisans show with profile images
- [ ] Image filenames visible below images

### Check Artisans Display
Verify these artisans have images:
- [ ] KSIC Silk Weavers
- [ ] Sri Krishna Murthy & Team
- [ ] Raghupathi Bhat
- [ ] Mysore Sandalwood Carvers Guild
- [ ] B.S. Yogiraj Shilpi
- [ ] Ramu Agarbathi Rollers

### Check Food Discovery
- [ ] Open: http://localhost:5000/food-discovery
- [ ] All 18 food places show in grid
- [ ] Each food item displays an image
- [ ] Images load properly

### Check Marketplace
- [ ] Open: http://localhost:5000/marketplace
- [ ] Click filter buttons
- [ ] Products display with images
- [ ] Artisan names visible

### Check Hidden Gems
- [ ] Open: http://localhost:5000/hidden-gems
- [ ] Click category filters
- [ ] Gems display with location images
- [ ] Map shows markers

## Step 7: Test Core Functionality

### Navigation
- [ ] Homepage loads: http://localhost:5000/
- [ ] Featured items display with images
- [ ] All navigation links work

### Features
- [ ] `/artisans/<id>` - View detailed artisan with products
- [ ] `/food-discovery` - Food filter buttons work
- [ ] Maps load properly (Leaflet)
- [ ] Forms submit without errors

### Images in Different Sections
- [ ] Artisan profiles: ✓ Images show
- [ ] Food discovery: ✓ Images show
- [ ] Products: ✓ Images show
- [ ] Locations/Gems: ✓ Images show
- [ ] Guides: ✓ Profile images show

## Step 8: Browser Cache Clear (if images not showing)
- [ ] Hard refresh browser: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- [ ] Close and reopen browser tab
- [ ] Clear browser cache if still not showing
- [ ] Restart Flask app: `Ctrl+C` then `python app.py`

## Troubleshooting Checklist

### If seed_data.py fails:
- [ ] Check Python version: `python --version` (need 3.6+)
- [ ] Check write permissions in project directory
- [ ] Delete old db: `rm mysore_unseen.db` (or `del mysore_unseen.db` on Windows)
- [ ] Re-run: `python seed_data.py`

### If image download fails:
- [ ] Check internet connection
- [ ] Verify requests installed: `pip install requests`
- [ ] Check console output for which items failed
- [ ] Retry: `python update_images_from_google.py`
- [ ] (May need to wait an hour if Google rate-limits)

### If images not showing on website:
- [ ] Hard refresh: `Ctrl+Shift+R`
- [ ] Check static folder exists: `ls static/images/`
- [ ] Restart Flask app
- [ ] Check browser console for 404 errors

### If application won't start:
- [ ] Check all dependencies: `pip install -r requirements.txt`
- [ ] Check if port 5000 is free
- [ ] Try different port: `flask run --port 5001`
- [ ] Check for syntax errors: `python -m py_compile app.py`

## Optional: Run Advanced Commands

### Fetch only specific sections:
```bash
# Only artisan images
python fetch_images_comprehensive.py --target artisans

# Only food images
python fetch_images_comprehensive.py --target food

# Only products
python fetch_images_comprehensive.py --target products
```

### Overwrite existing images:
```bash
python fetch_images_comprehensive.py --overwrite
```

### Analyze database:
```bash
python analyze_db.py
```

## Post-Setup

### Verify Everything Works
- [ ] Images display on /artisans
- [ ] Images display on /food-discovery
- [ ] Images display on /marketplace
- [ ] Images display on /hidden-gems
- [ ] All filters work
- [ ] Maps display correctly
- [ ] No broken image links (404 errors)

### Next Steps
- [ ] Explore all pages manually
- [ ] Test filters and navigation
- [ ] Click artisan names, food types, categories
- [ ] Verify links work correctly
- [ ] Check mobile responsiveness (browser dev tools)

### When Ready to Deploy
- [ ] Ensure `static/images/` included in deployment
- [ ] Ensure `mysore_unseen.db` included
- [ ] Deploy using gunicorn: `pip install gunicorn && gunicorn app:app`
- [ ] Or use Vercel: `npm install -g vercel && vercel`

## Success Indicators ✓

All of these should be true:
- ✓ 50+ JPG files in `static/images/`
- ✓ Database contains image_url for all items
- ✓ `/artisans` page displays 6 artisan images
- ✓ `/food-discovery` page displays 18 food images
- ✓ `/marketplace` page displays product images
- ✓ `/hidden-gems` page displays location images
- ✓ No 404 errors in browser console
- ✓ Images load quickly from local storage
- ✓ All pages render correctly
- ✓ Responsive design works on mobile

## Need Help?

**Quick Reference Files**:
- `QUICK_START.txt` - Quick command reference
- `IMAGES_SETUP.md` - Image setup guide
- `README.md` - Complete documentation
- `RUNNING_IMAGE_SCRIPTS.md` - Technical reference

**Common Issues**:
- Images not downloading? Check internet, try later
- Database won't create? Check write permissions
- Images not showing? Hard refresh browser
- App won't start? Check all dependencies installed

## Estimated Time

| Step | Time | Notes |
|------|------|-------|
| Install dependencies | 2 min | First-time only |
| Seed database | 1 min | Creates initial data |
| Fetch images | 15-20 min | Downloads 50+ images |
| Start application | 30 sec | Flask startup |
| Verify display | 5 min | Check images load |
| **Total** | **25-30 min** | One-time setup |

---

**✅ Setup Complete!** Your Mysore Unseen application now has full image support.

Next: `python app.py` then visit http://localhost:5000
