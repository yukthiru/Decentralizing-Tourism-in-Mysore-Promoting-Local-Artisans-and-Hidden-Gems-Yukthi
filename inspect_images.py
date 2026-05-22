import os

names = [
    'Lingambudhi_Lake.jpg',
    'Shuka_Vana_Parrot_Park.jpg',
    'Jayalakshmi_Vilas_Mansion_Folklore_Museum.jpg',
    'Melody_World_Wax_Museum.jpg',
    'Venugopala_Swamy_Temple.jpg',
    'Kunti_Betta.jpg',
    'Shuka_Vana_(Parrot_Park).jpg',
    'Lingambudhi_Lake.png',
]

for name in names:
    path = os.path.join('static', 'images', name)
    if os.path.exists(path):
        print(name, os.path.getsize(path))
    else:
        print(name, 'MISSING')
