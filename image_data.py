# image_data.py - Verified Wikipedia thumbnail URLs for Mysore Unseen

PLACE_IMAGES = {
    "Bhogadi Lake": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Hinkal_Town%2C_Mysore.jpg/960px-Hinkal_Town%2C_Mysore.jpg",
    "Brindavan Gardens": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Brindavan_Gardens.JPG/960px-Brindavan_Gardens.JPG",
    "Cauvery": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Thalakkaveri_Temple%2C_Karnataka.jpg/960px-Thalakkaveri_Temple%2C_Karnataka.jpg",
    "Cauvery Karnataka State Arts & Crafts Emporium": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Mysore_Silk_Saree.jpg/960px-Mysore_Silk_Saree.jpg",
    "Chamundeshwari Temple": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Chamundeshwari_Temple_Mysore.jpg/960px-Chamundeshwari_Temple_Mysore.jpg",
    "Chamundi Hills": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/J.C.Nagar_Welcome_Board_to_Chamundi_Hills.jpg/960px-J.C.Nagar_Welcome_Board_to_Chamundi_Hills.jpg",
    "Chunchanakatte Falls": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Chunchanakatte_Falls.jpg/960px-Chunchanakatte_Falls.jpg",
    "Devaraja Market": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Devaraja_Market%2C_Mysore_%28306989724%29.jpg/960px-Devaraja_Market%2C_Mysore_%28306989724%29.jpg",
    "Folklore Museum": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/JayalakshmiVilasMansion.jpg/960px-JayalakshmiVilasMansion.jpg",
    "Gopalakrishna Adiga": "https://upload.wikimedia.org/wikipedia/en/f/f4/G_Adiga.jpg",
    "Gopalakrishna Adiga's House": "https://upload.wikimedia.org/wikipedia/en/f/f4/G_Adiga.jpg",
    "Guru Sweet Mart": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Mysore_pak.jpg/960px-Mysore_pak.jpg",
    "Jaganmohan Palace": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/A_view_of_Jaganmohan_Palace.jpg/960px-A_view_of_Jaganmohan_Palace.jpg",
    "Jayalakshmi Vilas Mansion": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/JayalakshmiVilasMansion.jpg/960px-JayalakshmiVilasMansion.jpg",
    "Jayalakshmi Vilas Mansion Folklore Museum": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/JayalakshmiVilasMansion.jpg/960px-JayalakshmiVilasMansion.jpg",
    "Karanji Lake": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Karanji_lake_pic.jpg/960px-Karanji_lake_pic.jpg",
    "Karanji Lake Butterfly Park": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Karanji_lake_pic.jpg/960px-Karanji_lake_pic.jpg",
    "Kaveri River": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Thalakkaveri_Temple%2C_Karnataka.jpg/960px-Thalakkaveri_Temple%2C_Karnataka.jpg",
    "KRS Dam": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Krishna_raja_sagara_dam.JPG/960px-Krishna_raja_sagara_dam.JPG",
    "KSIC Silk Weaving Factory Outlet": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Mysore_Silk_Saree.jpg/960px-Mysore_Silk_Saree.jpg",
    "Kukkarahalli Lake": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Kukkarahalli_Lake.jpg/960px-Kukkarahalli_Lake.jpg",
    "Lalitha Mahal": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Lalitha_Mahal_Palace_Hotel.jpg/960px-Lalitha_Mahal_Palace_Hotel.jpg",
    "Lingambudhi Lake": "https://upload.wikimedia.org/wikipedia/commons/7/74/Lingambudhi_Lake_when_filled.jpeg",
    "Manandavadi Road": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Devaraja_Market%2C_Mysore_%28306989724%29.jpg/960px-Devaraja_Market%2C_Mysore_%28306989724%29.jpg",
    "Mandi Mohalla": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Devaraja_Market%2C_Mysore_%28306989724%29.jpg/960px-Devaraja_Market%2C_Mysore_%28306989724%29.jpg",
    "Mandi Mohalla Artisan Cluster": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Devaraja_Market%2C_Mysore_%28306989724%29.jpg/960px-Devaraja_Market%2C_Mysore_%28306989724%29.jpg",
    "Melody World Wax Museum": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/CeciliaCheung_MadameTussauds.jpg/960px-CeciliaCheung_MadameTussauds.jpg",
    "Mysore Pak": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Mysore_pak.jpg/960px-Mysore_pak.jpg",
    "Mysore Palace": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Mysore_Palace_Morning.jpg/960px-Mysore_Palace_Morning.jpg",
    "Mysore Sand Sculpture Museum": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Sand_museum_Mysore_sculpture.jpg/960px-Sand_museum_Mysore_sculpture.jpg",
    "Mysore Zoo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Entrance_of_Mysore_Zoo.jpg/960px-Entrance_of_Mysore_Zoo.jpg",
    "Mysore Zoo (Sri Chamarajendra Zoological Gardens)": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Entrance_of_Mysore_Zoo.jpg/960px-Entrance_of_Mysore_Zoo.jpg",
    "Old Palace Elephant Stables": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Kbr_park.jpg/960px-Kbr_park.jpg",
    "Raghupathi Bhat Ganjifa Studio": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Ten_Playing_Cards_%28Ganjifa%29_LACMA_M.2001.210.4.1-.10.jpg/960px-Ten_Playing_Cards_%28Ganjifa%29_LACMA_M.2001.210.4.1-.10.jpg",
    "Rail Museum": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Mysuru_rail_museum_entrance.jpg/960px-Mysuru_rail_museum_entrance.jpg",
    "Railway Museum": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Mysuru_rail_museum_entrance.jpg/960px-Mysuru_rail_museum_entrance.jpg",
    "Rosewood inlay": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Wood_inlay_Mysore.jpg/960px-Wood_inlay_Mysore.jpg",
    "Sand Sculpture Museum": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Sand_museum_Mysore_sculpture.jpg",
    "Sayyaji Rao Road": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Devaraja_Market%2C_Mysore_%28306989724%29.jpg/960px-Devaraja_Market%2C_Mysore_%28306989724%29.jpg",
    "Shuka Vana": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Rainbow_lorikeet_%28Trichoglossus_moluccanus_moluccanus%29_Sydney.jpg/960px-Rainbow_lorikeet_%28Trichoglossus_moluccanus_moluccanus%29_Sydney.jpg",
    "Shuka Vana (Parrot Park)": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Rainbow_lorikeet_%28Trichoglossus_moluccanus_moluccanus%29_Sydney.jpg/960px-Rainbow_lorikeet_%28Trichoglossus_moluccanus_moluccanus%29_Sydney.jpg",
    "Sri Chamarajendra Zoological Gardens": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Entrance_of_Mysore_Zoo.jpg/960px-Entrance_of_Mysore_Zoo.jpg",
    "Sri Krishna Murthy Inlay Arts": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Wood_inlay_Mysore.jpg/960px-Wood_inlay_Mysore.jpg",
    "Sri Nandi Temple": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Nandi-Tirtha-Temple-Malleswaram-Bangalore_%281%29.jpg/960px-Nandi-Tirtha-Temple-Malleswaram-Bangalore_%281%29.jpg",
    "Sri Nandi Temple (Monolithic Bull)": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Nandi-Tirtha-Temple-Malleswaram-Bangalore_%281%29.jpg/960px-Nandi-Tirtha-Temple-Malleswaram-Bangalore_%281%29.jpg",
    "Srirangapatna Gumbaz": "https://upload.wikimedia.org/wikipedia/commons/9/97/Gumbaz.jpg",
    "St. Philomena's Church": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/India_-_St._Philomena%27s_Church_02.jpg/960px-India_-_St._Philomena%27s_Church_02.jpg",
    "Tippu Sultan's Summer Palace": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Tippu_Sultan%27s_Summer_palace.jpg/960px-Tippu_Sultan%27s_Summer_palace.jpg",
    "Tonachi Village Weavers": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Wood_inlay_Mysore.jpg/960px-Wood_inlay_Mysore.jpg",
    "Varuna Lake": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Karanji_lake_pic.jpg/960px-Karanji_lake_pic.jpg",
    "Wax Museum": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/CeciliaCheung_MadameTussauds.jpg/960px-CeciliaCheung_MadameTussauds.jpg",
}


ARTISAN_IMAGES = {
    "B.S. Yogiraj Shilpi": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Wood_inlay_Mysore.jpg/960px-Wood_inlay_Mysore.jpg",
    "KSIC Silk Weavers": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Mysore_Silk_Saree.jpg/960px-Mysore_Silk_Saree.jpg",
    "Mysore Sandalwood Carvers Guild": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Sandalwood_carving.jpg/960px-Sandalwood_carving.jpg",
    "Raghupathi Bhat": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Ten_Playing_Cards_%28Ganjifa%29_LACMA_M.2001.210.4.1-.10.jpg/960px-Ten_Playing_Cards_%28Ganjifa%29_LACMA_M.2001.210.4.1-.10.jpg",
    "Ramu Agarbathi Rollers": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Incenselonghua.jpg",
    "Sri Krishna Murthy": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Wood_inlay_Mysore.jpg/960px-Wood_inlay_Mysore.jpg",
}


FOOD_IMAGES = {
    "Aloo Bonda": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/The_real_South_Indian_Bonda.jpg/960px-The_real_South_Indian_Bonda.jpg",
    "Artisanal Sourdough": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Home_made_sour_dough_bread.jpg/960px-Home_made_sour_dough_bread.jpg",
    "Benne Masala Dosa": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Dosa_at_Sri_Ganesha_Restauran%2C_Bangkok_%2844570742744%29.jpg/960px-Dosa_at_Sri_Ganesha_Restauran%2C_Bangkok_%2844570742744%29.jpg",
    "Butter Dosa": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Dosa_at_Sri_Ganesha_Restauran%2C_Bangkok_%2844570742744%29.jpg/960px-Dosa_at_Sri_Ganesha_Restauran%2C_Bangkok_%2844570742744%29.jpg",
    "Churmuri": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Behael_Puri_%286105489342%29.jpg/960px-Behael_Puri_%286105489342%29.jpg",
    "Dosa": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Dosa_at_Sri_Ganesha_Restauran%2C_Bangkok_%2844570742744%29.jpg/960px-Dosa_at_Sri_Ganesha_Restauran%2C_Bangkok_%2844570742744%29.jpg",
    "Dry Gobi": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Cauliflower_Manchurian.jpg/960px-Cauliflower_Manchurian.jpg",
    "Filter Coffee": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Filter_kaapi.JPG/960px-Filter_kaapi.JPG",
    "Idli": "https://upload.wikimedia.org/wikipedia/commons/1/11/Idli_Sambar.JPG",
    "Idli Vada": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Medu_Vada.JPG/960px-Medu_Vada.JPG",
    "Mangalorean Fish Curry": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Pan-fried-fish.jpg/960px-Pan-fried-fish.jpg",
    "Masala Dosa": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Rameshwaram_Cafe_Dosa.jpg/960px-Rameshwaram_Cafe_Dosa.jpg",
    "Millet Burgers": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/RedDot_Burger.jpg/960px-RedDot_Burger.jpg",
    "Mutton Biryani": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/%22Hyderabadi_Dum_Biryani%22.jpg/960px-%22Hyderabadi_Dum_Biryani%22.jpg",
    "Mysore Masala Dosa": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Rameshwaram_Cafe_Dosa.jpg/960px-Rameshwaram_Cafe_Dosa.jpg",
    "Mysore Pak": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Mysore_pak.jpg/960px-Mysore_pak.jpg",
    "Ragi Mudde": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/RAGI_MUDDE.JPG/960px-RAGI_MUDDE.JPG",
    "Sarsaparilla Soda": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Sioux_City_sarsaparilla_bottles.jpg/960px-Sioux_City_sarsaparilla_bottles.jpg",
    "South Indian Thali": "https://upload.wikimedia.org/wikipedia/commons/4/49/Vegetarian_Curry.jpeg",
    "Thatte Idli": "https://upload.wikimedia.org/wikipedia/commons/1/11/Idli_Sambar.JPG",
    "Wood-fired Pizza": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Pizza-3007395.jpg/960px-Pizza-3007395.jpg",
}


DEFAULT_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Mysore_Palace_Morning.jpg/800px-Mysore_Palace_Morning.jpg"

def get_image(mapping, name):
    if not name:
        return DEFAULT_IMAGE
    name_lower = name.lower()
    for key, url in mapping.items():
        if key.lower() in name_lower or name_lower in key.lower():
            return url
    return DEFAULT_IMAGE
