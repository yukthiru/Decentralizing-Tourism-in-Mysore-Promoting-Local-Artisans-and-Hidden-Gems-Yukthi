from app import app
from models import db, HiddenGem, Artisan, ArtisanProduct, LocalFood, StayOption, MarketStall, LocalGuide
import os
import re
import unicodedata

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'static', 'images')


def normalize_name_key(value):
    if not value:
        return ''
    value = unicodedata.normalize('NFKD', value)
    value = re.sub(r'[^A-Za-z0-9]+', '_', value).strip('_')
    value = re.sub(r'_+', '_', value)
    return value.lower()


def safe_image_filename(name):
    return normalize_name_key(name) + '.jpg'


def find_local_image_url(name):
    if not name:
        return None
    filename = safe_image_filename(name)
    candidate = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(candidate):
        return '/static/images/' + filename

    key = normalize_name_key(name)
    matches = []
    for f in os.listdir(IMAGE_DIR):
        base = os.path.splitext(f)[0]
        normalized = normalize_name_key(base)
        if normalized.startswith(key) or key in normalized:
            matches.append(f)
    if matches:
        matches.sort(key=lambda x: (len(x), x))
        return '/static/images/' + matches[0]
    return None


def attach_local_images(items, name_attr='name'):
    for item in items:
        current = getattr(item, 'image_url', None)
        if not current or current.startswith('/static/images/'):
            continue
        name = getattr(item, name_attr, None)
        local = find_local_image_url(name)
        if local:
            item.image_url = local
            if hasattr(item, 'image_credit'):
                item.image_credit = 'Local image'


def seed_data():
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        print("Creating fresh tables...")
        db.create_all()

        print("Seeding Obscure Hidden Gems & Locations...")
        gems = [
            HiddenGem(image_url="/static/images/Shuka_Vana__Parrot_Park_.jpg", image_credit="Local image", name="Shuka Vana (Parrot Park)", category="Nature", description="A unique rehabilitation center housing an astonishing variety of rare and colorful bird species in a sprawling aviary.", location="Datta Nagar", directions_url="https://maps.google.com/?q=Shuka+Vana+Mysore", is_featured=True, lat=12.2785, lng=76.6664, best_time_to_visit="Morning 9:30 AM", entry_fee="Free", local_tip="Make sure to get a photo with the macaws, and check out the hospital section where injured birds are treated."),
            HiddenGem(image_url="/static/images/Lingambudhi_Lake.jpg", image_credit="Local image", name="Lingambudhi Lake", category="Nature", description="A quiet, scenic oasis with lush surroundings on the outskirts of Mysore, ideal for those seeking peaceful, reflective moments away from the city noise.", location="Srirampura", directions_url="https://maps.google.com/?q=Lingambudhi+Lake+Mysore", is_featured=True, lat=12.2764, lng=76.6186, best_time_to_visit="Early Morning", entry_fee="Free", local_tip="Bring binoculars; it's a fantastic, undisturbed spot for bird watching during migration season."),
            HiddenGem(image_url="/static/images/Jayalakshmi_Vilas_Mansion_Folklore_Museum.jpg", image_credit="Local image", name="Jayalakshmi Vilas Mansion Folklore Museum", category="Heritage", description="A lesser-known architectural gem located within the university campus, housing a fascinating and extensive folklore museum.", location="Manasagangotri", directions_url="https://maps.google.com/?q=Jayalakshmi+Vilas+Mansion", is_featured=True, lat=12.3055, lng=76.6335, best_time_to_visit="Afternoon", entry_fee="₹15", local_tip="Look out for the collection of intricate wooden temple chariots stored inside."),
            HiddenGem(image_url="/static/images/Melody_World_Wax_Museum.jpg", image_credit="Local image", name="Melody World Wax Museum", category="Art", description="A quirky, offbeat attraction housed in a heritage building, showcasing an eclectic collection of antique musical instruments and life-size wax figures.", location="Kurubarahalli", directions_url="https://maps.google.com/?q=Melody+World+Wax+Museum+Mysore", is_featured=False, lat=12.3072, lng=76.6748, best_time_to_visit="Anytime", entry_fee="₹30", local_tip="A great, unusual spot if you have an interest in vintage brass bands and tribal instruments."),
            HiddenGem(image_url="/static/images/Venugopala_Swamy_Temple.jpg", image_credit="Local image", name="Venugopala Swamy Temple", category="Heritage", description="A stunning, recently relocated ancient temple situated right on the scenic backwaters of the KRS Dam.", location="KRS Backwaters", directions_url="https://maps.google.com/?q=Venugopala+Swamy+Temple+Mysore", is_featured=False, lat=12.4338, lng=76.5786, best_time_to_visit="Sunset", entry_fee="Free", local_tip="The drive here during the monsoon offers some of the most breathtaking views around Mysore."),
            HiddenGem(image_url="/static/images/Kunti_Betta.jpg", image_credit="Local image", name="Kunti Betta", category="Nature", description="A rugged, less-frequented hillock steeped in mythological significance, offering excellent short trekking and sunrise views.", location="Pandavapura", directions_url="https://maps.google.com/?q=Kunti+Betta", is_featured=False, lat=12.5020, lng=76.7110, best_time_to_visit="Night/Early Sunrise", entry_fee="Free", local_tip="Highly recommended for a night trek; the top offers a beautiful view of the surrounding lakes."),
            # Artisan Workshops Map Points (Kept obscure)
            HiddenGem(image_url="/static/images/Tonachi_Village_Weavers.jpg", image_credit="Local image", name="Tonachi Village Weavers", category="Artisan Workshop", description="A small village preserving traditional handloom weaving techniques, creating beautiful rustic cotton fabrics away from the commercial silk centers.", location="Tonachi Koppal", directions_url="https://maps.google.com/?q=Tonachikoppal+Mysore", is_featured=False, lat=12.3160, lng=76.6340, best_time_to_visit="Mid-day", entry_fee="Free", local_tip="You can directly buy fabric from the weavers at lower prices."),
            HiddenGem(image_url="/static/images/Sri_Krishna_Murthy_Inlay_Arts.jpg", image_credit="Local image", name="Sri Krishna Murthy Inlay Arts", category="Artisan Workshop", description="A traditional rosewood inlay workshop hidden in the narrow lanes of the historic Mandi Mohalla crafting district.", location="Mandi Mohalla", directions_url="https://maps.google.com/?q=Mandi+Mohalla+Mysore", is_featured=False, lat=12.3180, lng=76.6500, best_time_to_visit="11 AM - 5 PM", entry_fee="Free", local_tip="Watch how natural colored woods (no paint!) are used to create the paintings."),
            HiddenGem(image_url="/static/images/Raghupathi_Bhat_Ganjifa_Studio.jpg", image_credit="Local image", name="Raghupathi Bhat Ganjifa Studio", category="Artisan Workshop", description="Studio of the master artist who revived the dying art of Mysore Ganjifa miniature card painting.", location="Srirampura", directions_url="https://maps.google.com/?q=Srirampura+Mysore", is_featured=False, lat=12.2800, lng=76.6200, best_time_to_visit="By Appointment", entry_fee="Free", local_tip="Ask about the squirrel hair brushes used for the microscopic details."),
            HiddenGem(image_url="/static/images/Sand_Sculpture_Museum.jpg", image_credit="Local image", name="Sand Sculpture Museum", category="Art", description="A unique and whimsical museum displaying over 150 intricate sand sculptures created using only water and sand.", location="Chamundi Hill Road", directions_url="https://maps.google.com/?q=Sand+Sculpture+Museum+Mysore", is_featured=False, lat=12.2965, lng=76.6800, best_time_to_visit="Morning", entry_fee="₹40", local_tip="Look for the massive 15-foot sculpture of Lord Ganesha."),
            HiddenGem(image_url="/static/images/Varuna_Lake.jpg", image_credit="Local image", name="Varuna Lake", category="Nature", description="A beautiful lake popular among local adventure groups for kayaking and water sports, rarely visited by conventional tourists.", location="Varuna Village", directions_url="https://maps.google.com/?q=Varuna+Lake+Mysore", is_featured=False, lat=12.2740, lng=76.7110, best_time_to_visit="Early Morning", entry_fee="Free", local_tip="Perfect spot for a quiet sunrise paddle boarding session."),
            HiddenGem(image_url="/static/images/Chunchanakatte_Falls.jpg", image_credit="Local image", name="Chunchanakatte Falls", category="Nature", description="A stunning waterfall on the Kaveri river steeped in mythology, known for the roar of the falls contrasting with the silence of the adjacent ancient temple.", location="Chunchanakatte", directions_url="https://maps.google.com/?q=Chunchanakatte+Falls", is_featured=False, lat=12.4930, lng=76.2880, best_time_to_visit="Monsoon", entry_fee="Free", local_tip="The water here is said to have a yellowish tinge from the turmeric used by Goddess Sita."),
            HiddenGem(image_url="/static/images/Guru_Sweet_Mart.jpg", image_credit="Local image", name="Guru Sweet Mart", category="Food", description="The legendary origin of the authentic Mysore Pak, still run by the descendants of Kakasura Madappa, the palace cook who invented it.", location="Devaraja Market", directions_url="https://maps.google.com/?q=Guru+Sweet+Mart+Mysore", is_featured=True, lat=12.3090, lng=76.6495, best_time_to_visit="Anytime", entry_fee="Free", local_tip="Buy the soft Mysore Pak, it melts in your mouth!"),
            HiddenGem(image_url="/static/images/Sri_Nandi_Temple__Monolithic_Bull_.jpg", image_credit="Local image", name="Sri Nandi Temple (Monolithic Bull)", category="Spiritual", description="A massive 15-foot monolithic Nandi (bull) statue carved out of a single boulder on Chamundi Hill, dating back to 1659.", location="Chamundi Hill", directions_url="https://maps.google.com/?q=Nandi+Statue+Mysore", is_featured=True, lat=12.2855, lng=76.6710, best_time_to_visit="Early Morning", entry_fee="Free", local_tip="Walk down the ancient stone steps from here instead of taking the road for a scenic trek.")
        ]
        attach_local_images(gems)
        db.session.add_all(gems)

        print("Seeding Real Artisans...")
        artisans = [
            Artisan(image_url="https://source.unsplash.com/800x600/?silk,weaving,India", image_credit="Image source: Unsplash", name="KSIC Silk Weavers", craft="Mysore Silk Weaving", years_experience=110, short_bio="Heritage weavers of the royal Mysore silk sari.", bio="The Karnataka Silk Industries Corporation (KSIC) factory was founded in 1912 by the Maharaja of Mysore. It employs generations of master weavers who specialize in pure silk woven with pure gold zari (65% silver and 0.65% gold).", contact_email="ksic.mysore@example.com", whatsapp=""),
            Artisan(image_url="https://source.unsplash.com/800x600/?wood,inlay,craft", image_credit="Image source: Unsplash", name="Sri Krishna Murthy & Team", craft="Rosewood Inlay Art", years_experience=45, short_bio="Creating poetry in wood with GI-tagged traditional inlay techniques.", bio="Based in Mandi Mohalla, this team specializes in the GI-tagged Mysore rosewood inlay. The craft involves cutting intricate designs into rosewood and fitting contrasting colored woods and acrylics perfectly into the gaps.", contact_email="mysore.inlay@example.com", whatsapp=""),
            Artisan(image_url="https://source.unsplash.com/800x600/?painting,art,India", image_credit="Image source: Unsplash", name="Raghupathi Bhat", craft="Ganjifa Card Painting", years_experience=50, short_bio="The master who revived the royal Ganjifa card art.", bio="Raghupathi Bhat is credited with single-handedly reviving the dying art of Mysore Ganjifa (ancient playing cards). He uses natural dyes extracted from leaves and flowers, and paints with brushes made of squirrel hair.", contact_email="ganjifa.art@example.com", whatsapp=""),
            Artisan(image_url="https://source.unsplash.com/800x600/?sandalwood,carving", image_credit="Image source: Unsplash", name="Mysore Sandalwood Carvers Guild", craft="Sandalwood Carving", years_experience=80, short_bio="Carving intricate tales in fragrant authentic sandalwood.", bio="A collective of state and national award-winning artisans who specialize in sculpting deities, boxes, and intricate garlands from government-sourced pure sandalwood.", contact_email="cauvery.crafts@example.com", whatsapp=""),
            Artisan(image_url="https://source.unsplash.com/800x600/?stone,sculpture,India", image_credit="Image source: Unsplash", name="B.S. Yogiraj Shilpi", craft="Traditional Sculpture", years_experience=60, short_bio="Master sculptor continuing the Shilpashastra tradition.", bio="Yogiraj Shilpi comes from a long lineage of palace sculptors. His family has carved many of the iconic statues seen around Mysore, utilizing traditional texts to perfect the proportions.", contact_email="shilpi.studio@example.com", whatsapp=""),
            Artisan(image_url="https://source.unsplash.com/800x600/?incense,handmade,India", image_credit="Image source: Unsplash", name="Ramu Agarbathi Rollers", craft="Incense Making", years_experience=30, short_bio="Hand-rolling the fragrant essence of Mysore.", bio="Before machine-made incense took over, Mysore's economy thrived on hand-rolled agarbathis. This collective still rolls traditional halmaddi and sandalwood paste onto bamboo splints by hand.", contact_email="ramu.aroma@example.com", whatsapp="")
        ]
        attach_local_images(artisans)
        db.session.add_all(artisans)
        db.session.commit() # Commit to get IDs

        print("Seeding Authentic Artisan Products...")
        products = [
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?silk,saree,India", image_credit="Image source: Unsplash", artisan_id=1, product_name="Mysore Crepe Silk Saree", description="Pure crepe silk with 100% pure gold zari border.", price_inr=15000, category="Silk"),
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?silk,stole,India", image_credit="Image source: Unsplash", artisan_id=1, product_name="Silk Georgette Stole", description="Lightweight authentic silk stole.", price_inr=2500, category="Silk"),
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?bridal,saree,India", image_credit="Image source: Unsplash", artisan_id=1, product_name="Heritage Bridal Saree", description="Heavy gold zari work traditional bridal wear.", price_inr=45000, category="Silk"),
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?wood,elephant,art", image_credit="Image source: Unsplash", artisan_id=2, product_name="Rosewood Elephant Dasara", description="Intricate inlay showing the Dasara elephant procession.", price_inr=3200, category="Wood"),
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?wood,painting,India", image_credit="Image source: Unsplash", artisan_id=2, product_name="Village Landscape Panel", description="Wall art depicting rural Karnataka in wood.", price_inr=6500, category="Wood"),
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?wood,box,India", image_credit="Image source: Unsplash", artisan_id=2, product_name="Octagonal Jewelry Box", description="Rosewood box with floral inlay.", price_inr=1800, category="Wood"),
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?sandalwood,incense", image_credit="Image source: Unsplash", artisan_id=6, product_name="Pure Sandalwood Agarbathi", description="100 sticks of hand-rolled pure sandalwood scent.", price_inr=350, category="Incense"),
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?dhoop,incense", image_credit="Image source: Unsplash", artisan_id=6, product_name="Mysore Jasmine Dhoop", description="Hand rolled natural Mysore Mallige dhoop cones.", price_inr=200, category="Incense"),
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?cards,ancient,art", image_credit="Image source: Unsplash", artisan_id=3, product_name="Dashavatara Ganjifa Set", description="Traditional 10-suit circular playing cards painted with natural dyes.", price_inr=12000, category="Painting"),
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?framed,art,India", image_credit="Image source: Unsplash", artisan_id=3, product_name="Ganjifa Mini Framed Art", description="Single Ganjifa card framed as wall art.", price_inr=1500, category="Painting"),
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?bronze,statue,India", image_credit="Image source: Unsplash", artisan_id=5, product_name="Panchaloha Nataraja", description="Lost-wax casting, 8 inches tall traditional bronze.", price_inr=8500, category="Metal"),
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?stone,ganesha,India", image_credit="Image source: Unsplash", artisan_id=5, product_name="Hoysala Style Ganesha", description="Soapstone carving in traditional Hoysala style.", price_inr=4500, category="Wood"), # Mixed category for simplicity
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?krishna,wood,statue", image_credit="Image source: Unsplash", artisan_id=4, product_name="Sandalwood Krishna Idol", description="Fragrant 4-inch carving from authentic wood.", price_inr=8500, category="Sandalwood"),
            ArtisanProduct(image_url="https://source.unsplash.com/800x600/?prayer,beads,India", image_credit="Image source: Unsplash", artisan_id=4, product_name="Sandalwood Mala", description="Traditional prayer beads.", price_inr=2200, category="Sandalwood")
        ]
        attach_local_images(products, name_attr='product_name')
        db.session.add_all(products)

        print("Seeding Obscure Local Food Discoveries...")
        foods = [
            LocalFood(image_url="/static/images/Tegu_Mess.jpg", image_credit="Local image", name="Tegu Mess", food_type="Home Kitchen", description="An iconic 'mess' style eatery tucked away in a residential area, serving incredible nati-style (country style) non-vegetarian meals on a banana leaf.", specialty_dish="Chicken Chops & Ragi Mudde", price_range="₹₹", location="Vontikoppal", lat=12.3250, lng=76.6350, open_hours="12:30 PM - 3:30 PM", is_vegetarian=False, local_secret="Eat the Ragi Mudde the traditional way: swallow it in small balls without chewing."),
            LocalFood(image_url="/static/images/Brahmin_s_Soda_Factory.jpg", image_credit="Local image", name="Brahmin's Soda Factory", food_type="Street Food", description="A vintage refreshment stall serving unique fruit sodas and milkshakes. Far less famous than the big sweet shops, but a local staple.", specialty_dish="Sarsaparilla Soda", price_range="₹", location="Near Suburban Bus Stand", lat=12.3080, lng=76.6550, open_hours="10 AM - 10 PM", is_vegetarian=True, local_secret="Try the 'Fruit Salad with Ice Cream', a classic old-school dessert that hasn't changed in decades."),
            LocalFood(image_url="/static/images/Anima_Bhavan.jpg", image_credit="Local image", name="Anima Bhavan", food_type="Dhaba", description="A completely unassuming spot that serves some of the most authentic traditional banana leaf meals, frequented only by locals.", specialty_dish="South Indian Thali", price_range="₹", location="Kalidasa Road", lat=12.3210, lng=76.6240, open_hours="12 PM - 3 PM", is_vegetarian=True, local_secret="Unlimited rice and excellent obbattu (sweet flatbread). Go early before the curries run out."),
            LocalFood(image_url="/static/images/Poojari_s_Fish_Land.jpg", image_credit="Local image", name="Poojari's Fish Land", food_type="Dhaba", description="Hidden on the highway outskirts, this place serves incredibly fresh coastal Karnataka seafood that you won't find in the city center.", specialty_dish="Mangalorean Fish Curry", price_range="₹₹", location="Bangalore-Mysore Highway", lat=12.3550, lng=76.6600, open_hours="11 AM - 10 PM", is_vegetarian=False, local_secret="The Neer Dosa paired with their fiery fish curry is the best combination here."),
            LocalFood(image_url="/static/images/Sri_Durga_Bhavan.jpg", image_credit="Local image", name="Sri Durga Bhavan", food_type="Street Food", description="A tiny, easily missed eatery near the zoo that serves incredibly soft idlis and a unique, watery but highly flavorful sambar.", specialty_dish="Thatte Idli", price_range="₹", location="Nazarbad", lat=12.3020, lng=76.6680, open_hours="6:30 AM - 11 AM", is_vegetarian=True, local_secret="They serve idlis on a dried leaf plate which imparts a subtle earthy flavor."),
            LocalFood(image_url="/static/images/Bonda_Mane.jpg", image_credit="Local image", name="Bonda Mane", food_type="Street Food", description="Literally 'The House of Bondas', a tiny garage converted into a bustling evening snack spot deep in a residential layout.", specialty_dish="Aloo Bonda & Mirchi Bajji", price_range="₹", location="Saraswathipuram", lat=12.2980, lng=76.6310, open_hours="4 PM - 8 PM", is_vegetarian=True, local_secret="Pair your bondas with their strong, frothy filter coffee."),
            LocalFood(image_url="/static/images/Mahadeshwara_Butter_Dosa.jpg", image_credit="Local image", name="Mahadeshwara Butter Dosa", food_type="Street Food", description="A fierce, lesser-known competitor to Mylari, serving crispy, butter-drenched dosas out of a very basic setup.", specialty_dish="Benne Masala Dosa", price_range="₹", location="Paduvarahalli", lat=12.3210, lng=76.6240, open_hours="7 AM - 12 PM", is_vegetarian=True, local_secret="Ask them to make it 'extra roast' for a perfect crunch."),
            LocalFood(image_url="/static/images/Depth_N_Green.jpg", image_credit="Local image", name="Depth N Green", food_type="Cafe", description="A hidden gem in the yoga district, blending global healthy tastes with local ingredients in a quiet, leafy setting.", specialty_dish="Millet Burgers", price_range="₹₹₹", location="Gokulam", lat=12.3361, lng=76.6268, open_hours="8 AM - 9 PM", is_vegetarian=True, local_secret="Their homemade kombucha is fantastic after a morning yoga session."),
            LocalFood(image_url="/static/images/Malgudi_Cafe.jpg", image_credit="Local image", name="Malgudi Cafe", food_type="Cafe", description="A quiet, beautifully restored heritage cafe run exclusively by women from marginalized backgrounds, set in the gardens of the Green Hotel.", specialty_dish="Filter Coffee & Homemade Cakes", price_range="₹₹", location="Jayalakshmipuram", lat=12.3235, lng=76.6205, open_hours="10 AM - 7 PM", is_vegetarian=True, local_secret="All profits go entirely to charitable and environmental projects in the region."),
            LocalFood(image_url="/static/images/Mahesh_Prasad_food.jpg", image_credit="Local image", name="Mahesh Prasad", food_type="Street Food", description="While extremely popular with local Mysoreans, it's virtually unknown to tourists. It serves excellent traditional South Indian fare.", specialty_dish="Open Butter Masala Dosa", price_range="₹", location="Ballal Circle", lat=12.2970, lng=76.6430, open_hours="6 AM - 10:30 PM", is_vegetarian=True, local_secret="They have a separate section for their delicious Mangalore buns and strong filter coffee."),
            LocalFood(image_url="/static/images/Sapa_Bakery___Cafe.jpg", image_credit="Local image", name="Sapa Bakery & Cafe", food_type="Cafe", description="A brilliant artisanal bakery hidden in a quiet neighborhood, known for bringing European-level sourdough and pastries to Mysore.", specialty_dish="Artisanal Sourdough & Pastries", price_range="₹₹₹", location="Saraswathipuram", lat=12.2980, lng=76.6350, open_hours="10 AM - 9 PM", is_vegetarian=False, local_secret="Their weekend specials sell out fast, so arrive early if you want the best selection."),
            LocalFood(image_url="/static/images/The_Old_House.jpg", image_credit="Local image", name="The Old House", food_type="Cafe", description="Set in a stunning 100-year-old heritage home, this rustic cafe is a fantastic escape offering wood-fired pizzas in a lush courtyard.", specialty_dish="Wood-fired Pizza & Tiramisu", price_range="₹₹₹", location="Chamarajapuram", lat=12.3010, lng=76.6420, open_hours="11 AM - 10 PM", is_vegetarian=True, local_secret="The ambiance at night under the fairy lights in the courtyard is unmatched."),
            LocalFood(image_url="/static/images/Hotel_RRR_food.jpg", image_credit="Local image", name="Hotel RRR", food_type="Dhaba", description="A legendary, bustling spot famous for serving authentic, fiery Andhra-style meals on traditional banana leaves.", specialty_dish="Mutton Biryani & Andhra Meals", price_range="₹₹", location="Gandhi Square", lat=12.3082, lng=76.6540, open_hours="11:30 AM - 4 PM, 7 PM - 10 PM", is_vegetarian=False, local_secret="Be prepared to wait; locals swear the long queue is always worth it."),
            LocalFood(image_url="/static/images/Amruth_Gobi_Centre.jpg", image_credit="Local image", name="Amruth Gobi Centre", food_type="Street Food", description="A massively popular evening street food cart known for pioneering Indian-Chinese street food in the city.", specialty_dish="Dry Gobi Manchurian", price_range="₹", location="Vontikoppal", lat=12.3255, lng=76.6355, open_hours="5 PM - 10 PM", is_vegetarian=True, local_secret="Pair the crispy Gobi with their spicy, tangy green chutney."),
            LocalFood(image_url="/static/images/Lakshman_Mess.jpg", image_credit="Local image", name="Lakshman Mess", food_type="Home Kitchen", description="A modest, no-frills setup popular with students and locals, highly regarded for authentic Naati-style (local rustic/country-style) non-vegetarian food.", specialty_dish="Mutton Chops & Ragi Mudde", price_range="₹₹", location="Santhepete Road", lat=12.3060, lng=76.6500, open_hours="12:00 PM - 4:00 PM, 7:00 PM - 10:30 PM", is_vegetarian=False, local_secret="Must-tries include Mutton Chops and Ragi Mudde with Naati Saaru (spicy curry)."),
            LocalFood(image_url="/static/images/Usman_Dry_Gobi.jpg", image_credit="Local image", name="Usman Dry Gobi", food_type="Street Food", description="A beloved street food cart that turned a simple cauliflower dish into a local sensation.", specialty_dish="Dry Gobi", price_range="₹", location="Chamrajpura", lat=12.3076, lng=76.6479, open_hours="6:00 PM - 10:30 PM", is_vegetarian=True, local_secret="The coating is extra crispy and seasoned perfectly, served with green chutney, onions, and cucumber."),
            LocalFood(image_url="/static/images/Mahesh_Prasad_food.jpg", image_credit="Local image", name="Raju's Kadai", food_type="Street Food", description="A lively local joint serving spicy Indo-Chinese street food favorites late into the evening.", specialty_dish="Chicken Manchurian", price_range="₹", location="Vontikoppal", lat=12.3258, lng=76.6352, open_hours="5 PM - 11 PM", is_vegetarian=False, local_secret="Order the extra-spicy chicken manchurian with fried rice for an authentic late-night treat."),
            LocalFood(image_url="/static/images/Guru_Sweet_Mart_market.jpg", image_credit="Local image", name="Lakshmi Tea Stall", food_type="Street Food", description="A tiny roadside stall with a huge personality, known for its strong masala chai and buttery bun sandwiches.", specialty_dish="Masala Chai & Bread Pakora", price_range="₹", location="Devaraja Market", lat=12.3091, lng=76.6497, open_hours="6 AM - 9 PM", is_vegetarian=True, local_secret="Sit down at the tiny shared table and enjoy the tea like a local.")
        ]
        attach_local_images(foods)
        db.session.add_all(foods)

        print("Seeding Authentic Stay Options...")
        stays = [
            StayOption(image_url="https://source.unsplash.com/800x600/?hostel,heritage,India", image_credit="Image source: Unsplash", name="Mansion 1907", type="Hostel", price_per_night_inr=600, location="Nazarbad", amenities="Vintage Architecture, Yoga Space, Bunk Beds"),
            StayOption(image_url="https://source.unsplash.com/800x600/?heritage,hotel,India", image_credit="Image source: Unsplash", name="Green Hotel", type="Heritage Hotel", price_per_night_inr=5500, location="Jayalakshmipuram", amenities="Restored Palace, Solar Heated, Profits go to charity"),
            StayOption(image_url="https://source.unsplash.com/800x600/?hotel,room,India", image_credit="Image source: Unsplash", name="Roopa Elite", type="Mid-range", price_per_night_inr=3500, location="Vontikoppal", amenities="Rooftop Pool, Modern Rooms, Great Breakfast"),
            StayOption(image_url="https://source.unsplash.com/800x600/?palace,hotel,India", image_credit="Image source: Unsplash", name="Lalitha Mahal Palace Hotel", type="Heritage Hotel", price_per_night_inr=12000, location="Chamundi Hill Road", amenities="Actual Royal Palace, Vintage Elevators, Fine Dining"),
            StayOption(image_url="https://source.unsplash.com/800x600/?hostel,backpacker,India", image_credit="Image source: Unsplash", name="Sonder Hostel", type="Hostel", price_per_night_inr=700, location="Gokulam", amenities="Digital Nomad Friendly, Fast WiFi, Cafe"),
            StayOption(image_url="https://source.unsplash.com/800x600/?hotel,pool,India", image_credit="Image source: Unsplash", name="Southern Star", type="Mid-range", price_per_night_inr=4500, location="Vinoba Road", amenities="Central Location, Pool, Multiple Restaurants")
        ]
        attach_local_images(stays)
        db.session.add_all(stays)

        print("Seeding Real Market Stalls & Artisan Markets...")
        stalls = [
            MarketStall(image_url="https://source.unsplash.com/800x600/?crafts,shop,India", image_credit="Image source: Unsplash", stall_name="Cauvery Karnataka State Arts & Crafts Emporium", market_area="Sayyaji Rao Road", stall_type="Government Emporium", products_sold="Authentic Sandalwood, Rosewood Inlay, Silk", open_days="Mon-Sat", open_time="10:00 AM - 8:00 PM", story="The most reliable government-operated enterprise under the Karnataka State Handicrafts Development Corporation for genuine, high-quality local crafts."),
            MarketStall(image_url="https://source.unsplash.com/800x600/?workshop,craft,India", image_credit="Image source: Unsplash", stall_name="Mandi Mohalla Artisan Cluster", market_area="Mandi Mohalla", stall_type="Traditional Workshops", products_sold="Rosewood Inlay Furniture, Wall Panels", open_days="Mon-Sat", open_time="11:00 AM - 6:00 PM", story="The historic heart of Mysore's world-famous GI-tagged rosewood inlay craft. You can see artisans working right on the streets."),
            MarketStall(image_url="https://source.unsplash.com/800x600/?sweetshop,India", image_credit="Image source: Unsplash", stall_name="Guru Sweet Mart", market_area="Sayyaji Rao Road", stall_type="Sweets", products_sold="Mysore Pak, Dharwad Peda", open_days="Daily", open_time="10 AM - 10 PM", story="Inventors of the Mysore Pak."),
            MarketStall(image_url="https://source.unsplash.com/800x600/?market,India", image_credit="Image source: Unsplash", stall_name="Devaraja Historic Market", market_area="Devaraja Market", stall_type="Traditional Market", products_sold="Mysore Mallige (Jasmine), Spices, Essential Oils", open_days="Daily", open_time="6 AM - 8:30 PM", story="A chaotic, authentic, and sensory-rich 130-year-old market giving a glimpse into everyday Mysore life."),
            MarketStall(image_url="https://source.unsplash.com/800x600/?silk,showroom,India", image_credit="Image source: Unsplash", stall_name="KSIC Silk Weaving Factory Outlet", market_area="Manandavadi Road", stall_type="Textiles", products_sold="Authentic Mysore Silk Saris", open_days="Mon-Sat", open_time="10:30 AM - 7:30 PM", story="The official factory outlet where you can ensure you are buying genuine, high-quality 100% pure gold zari silk.")
        ]
        attach_local_images(stalls, name_attr='stall_name')
        db.session.add_all(stalls)

        print("Seeding Local Tour Guides...")
        guides = [
            LocalGuide(name="Venkatesh V.V.", expertise="Heritage & Architecture", languages="English, Hindi, French", description="A highly recommended independent guide known for deep knowledge of Mysore's history, palace architecture, and offbeat sights like local schools and farms.", contact_info="ToursByLocals Profile", image_url="/static/images/Local_Guide_Default.jpg", image_credit="Local image", rating=4.9, is_certified=True),
            LocalGuide(name="Unventured Trails", expertise="Cycling & Cultural Walks", languages="English, Kannada", description="An experiential tour company specializing in safe, immersive cycling tours and heritage walks that explore the authentic culture and hidden alleys of Mysore.", contact_info="unventured.com", image_url="/static/images/Local_Guide_Default.jpg", image_credit="Local image", rating=4.8, is_certified=True),
            LocalGuide(name="Royal Mysore Walks", expertise="Walking Tours & Food Walks", languages="English, Hindi, Kannada", description="Pioneers of walking tours in Mysore, offering everything from the classic Royal Walk to intricate artisan and food discovery trails.", contact_info="royalmysorewalks.com", image_url="/static/images/Local_Guide_Default.jpg", image_credit="Local image", rating=4.7, is_certified=True),
            LocalGuide(name="Gulzar Bano", expertise="Artisan & Market Tours", languages="English, Urdu, Hindi", description="A dedicated local guide with extensive connections in the artisan community, specializing in rosewood inlay workshops and the historic Devaraja Market.", contact_info="tourHQ Profile", image_url="/static/images/Local_Guide_Default.jpg", image_credit="Local image", rating=4.8, is_certified=True)
        ]
        attach_local_images(guides)
        db.session.add_all(guides)

        db.session.commit()
        print("Database fully seeded with real Mysore data!")

if __name__ == "__main__":
    seed_data()
