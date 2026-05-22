# Mysore Unseen 🌍 - Decentralizing Tourism

A Flask-based web application promoting local artisans, hidden gems, and authentic food experiences in Mysore, Karnataka.

## ⚡ Quick Start (3 Steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed database and fetch images
python seed_data.py
python update_images_from_google.py

# 3. Run application
python app.py
```

Open http://localhost:5000 to explore!

## 🎨 Features

### Artisan Explore
Browse and connect with Mysore's master craftspeople:
- **Silk Weavers** - Royal Mysore silk saris with pure gold zari
- **Rosewood Inlay Artists** - GI-tagged traditional wood art
- **Ganjifa Card Painters** - Ancient miniature card painting revival
- **Sandalwood Carvers** - Fragrant traditional sculpture
- **Sculptors** - Traditional Shilpashastra art form
- **Incense Makers** - Hand-rolled traditional agarbathi

**Images**: Automatically fetched from Google Images ✓

### 🍴 Food Discovery
Discover authentic local food far from tourist traps:
- **Street Food**: Bondas, dosas, gobi, tea stalls
- **Dhabas**: Traditional banana leaf meals
- **Sweet Shops**: Mysore Pak origin (Guru Sweet Mart)
- **Cafes**: Modern healthy options and heritage cafes
- **Specialty**: Fish curry, biryani, idlis, and more

18+ locations with detailed descriptions, GPS coordinates, and opening hours.

**Images**: Automatically fetched from Google Images ✓

### 💎 Hidden Gems
13 off-beat destinations including:
- Nature reserves (Shuka Vana parrot park, Lingambudhi Lake)
- Heritage sites (Jayalakshmi Vilas, Melody World Museum)
- Spiritual locations (Venugopala Temple, Nandi Statue)
- Art galleries (Sand Sculpture Museum)
- Artisan workshops (Ganjifa Studio, Rosewood workshops)

### 🛍️ Marketplace
Browse and purchase directly from artisans:
- 14+ products from local craftspeople
- Direct WhatsApp contact integration
- Price transparency
- Product descriptions and artisan profiles

### 🗺️ Interactive Features
- **Leaflet Maps** - Explore locations on interactive maps
- **AI Walking Tours** - Google Gemini powered tour generation
- **Itinerary Planner** - Multi-day custom tour planning
- **Local Guides** - Connect with professional tour guides
- **Stay Options** - Hotels and hostels curated for travelers

## 📋 What's New (Image Support)

✨ **All items now have images!**

- ✓ 6 Artisan profiles with photos
- ✓ 18 Food establishments with cuisine photos
- ✓ 14 Artisan product photos
- ✓ 13 Hidden gem location photos
- ✓ 6 Market stall photos

**Setup images in one command:**
```bash
python update_images_from_google.py
```

See [IMAGES_SETUP.md](IMAGES_SETUP.md) for details.

## 🏗️ Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Python 3
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Maps**: Leaflet.js, OpenStreetMap
- **AI**: Google Gemini API (optional, fallback included)
- **Image Fetching**: Google Images web scraper
- **Hosting**: Vercel ready

## 📦 Project Structure

```
mysore-unseen/
├── app.py                          # Flask app & API routes
├── models.py                       # Database models
├── seed_data.py                    # Initial data seeding
├── update_images_from_google.py    # ← Fetch images (NEW!)
├── requirements.txt                # Dependencies
├── static/
│   ├── images/                     # Downloaded images (50+)
│   ├── style.css                   # Styling
│   └── script.js                   # Frontend logic
├── templates/
│   ├── artisans.html              # Artisan listings
│   ├── food_discovery.html        # Food with maps
│   ├── marketplace.html           # Product marketplace
│   ├── hidden_gems.html           # Hidden gems explorer
│   ├── walking_tour.html          # Tour generator
│   └── ... (6 more pages)
├── IMAGES_SETUP.md                # Image setup guide
├── RUNNING_IMAGE_SCRIPTS.md       # Technical guide
└── QUICK_START.txt                # Quick reference
```

## 🚀 Usage

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python seed_data.py

# Fetch images (15-20 mins, one-time only)
python update_images_from_google.py

# Run locally
python app.py
```

Visit http://localhost:5000 in your browser.

### Deployment (Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Deployment (Traditional Server)

```bash
pip install gunicorn
gunicorn app:app
```

## 📱 Pages & Routes

| Route | Description |
|-------|-------------|
| `/` | Homepage with featured items |
| `/explore` | Browse hidden gems with filters |
| `/artisans` | **Artisan profiles with images** |
| `/artisans/<id>` | Detailed profile & products |
| `/food-discovery` | **Food places with map & images** |
| `/marketplace` | Product marketplace |
| `/walking-tour` | AI-powered tour generator |
| `/tour-planner` | Itinerary planner |
| `/guides` | Local tour guide profiles |
| `/contact` | Contact form |

## 🔌 API Endpoints

### Data APIs
- `GET /api/gems` - Hidden gems (filter by category)
- `GET /api/food` - Food places (filter by type, vegetarian)
- `GET /api/artisans` - All artisans
- `GET /api/products` - Products (by category or artisan)
- `GET /api/guides` - Tour guides

### Tour APIs
- `POST /api/generate-tour` - AI walking tour
- `POST /api/plan-tour` - Multi-day itinerary

### Maps
- `GET /api/gems/map` - Map data for locations

## 🖼️ Image Management

### Automatic Image Fetching

All items have images fetched from Google Images automatically:

```bash
python update_images_from_google.py
```

**What it does:**
1. Searches Google Images for each artisan, food place, product
2. Downloads images locally to `static/images/`
3. Updates database with image URLs
4. Takes ~15-20 minutes (1.5s delays between requests)

**First run:** ~20 minutes
**Subsequent runs:** Skip existing images, run in seconds

### Adding New Items

```python
# 1. Edit seed_data.py - add new artisan/food item
# 2. Run seed_data.py to update database
# 3. Run image fetcher to get images
python seed_data.py
python update_images_from_google.py
# 4. Restart app
```

See [IMAGES_SETUP.md](IMAGES_SETUP.md) for detailed guide.

## ⚙️ Configuration

### Environment Variables
```bash
# Optional: Add Gemini API key for AI tours
export GEMINI_API_KEY=your_key_here
```

If not set, the app uses built-in fallback responses.

### Database
- Type: SQLite3
- Location: `mysore_unseen.db`
- Auto-created on first run

## 🐛 Troubleshooting

### Images not showing?
1. Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Check: `ls static/images/*.jpg`
3. Restart Flask app

### Database not updating?
1. Delete and reseed: `rm mysore_unseen.db && python seed_data.py`
2. Re-fetch images: `python update_images_from_google.py`

### Image fetcher failing?
1. Check internet connection
2. Try later (may hit Google Images rate limit)
3. See [RUNNING_IMAGE_SCRIPTS.md](RUNNING_IMAGE_SCRIPTS.md) for advanced options

## 📚 Documentation

- **[IMAGES_SETUP.md](IMAGES_SETUP.md)** - Quick image setup guide
- **[RUNNING_IMAGE_SCRIPTS.md](RUNNING_IMAGE_SCRIPTS.md)** - Technical reference
- **[IMAGE_IMPLEMENTATION_SUMMARY.md](IMAGE_IMPLEMENTATION_SUMMARY.md)** - Complete details
- **[QUICK_START.txt](QUICK_START.txt)** - Command reference

## 💡 Key Features Explained

### AI-Powered Tours
- Uses Google Gemini API (optional)
- Fallback responses if API unavailable
- Customizable by interests, duration, and pace

### Direct Artisan Contact
- WhatsApp integration for inquiries
- Email addresses for professionals
- Product inquiry tracking

### Geo-Location Support
- Latitude/longitude for all places
- OpenStreetMap integration
- Walking directions to nearby locations

### SEO Friendly
- Clean URLs and routes
- Semantic HTML
- Mobile responsive design

## 🤝 Contributing

To add new artisans or food places:

1. Fork/clone the repository
2. Edit `seed_data.py` with new entries
3. Run `python seed_data.py`
4. Run `python update_images_from_google.py`
5. Test locally with `python app.py`
6. Commit and push

## 📝 License

[Specify your license here]

## 🎯 Roadmap

- [x] Basic artisan & food discovery
- [x] Image support for all items
- [ ] User authentication
- [ ] Booking system
- [ ] Review & ratings
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Payment integration

## 📧 Support

For questions or issues:
1. Check documentation in project root
2. Visit `/contact` page to send message
3. Review [IMAGES_SETUP.md](IMAGES_SETUP.md) for image questions

---

**Made with ❤️ to support Mysore's local artisans and authentic experiences**

**Latest Update**: Image support added with automatic Google Images fetching
