#!/usr/bin/env python
"""Analyze what artisans and food items need images."""

import sqlite3
import os

DB_PATH = r'c:\Users\Yukthi R U\Downloads\inunity antigravity\mysore-unseen\mysore_unseen.db'

def analyze():
    """Check database for missing images."""
    if not os.path.exists(DB_PATH):
        print("Database doesn't exist yet. Running seed_data first...")
        import sys
        sys.path.insert(0, os.path.dirname(DB_PATH))
        from seed_data import seed_data
        seed_data()
        print("✓ Database created and seeded!")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check artisans
    print("\n" + "="*60)
    print("ARTISANS")
    print("="*60)
    cursor.execute('SELECT id, name, craft, image_url FROM artisan ORDER BY id')
    artisans = cursor.fetchall()
    
    artisans_needing_images = []
    for a in artisans:
        print(f"{a['id']:2d}. {a['name']:30s} | {a['craft']:25s} | {a['image_url'][:50] if a['image_url'] else 'MISSING'}")
        if not a['image_url'] or not a['image_url'].startswith('/static/images/'):
            artisans_needing_images.append((a['id'], a['name']))
    
    # Check food
    print("\n" + "="*60)
    print("LOCAL FOOD")
    print("="*60)
    cursor.execute('SELECT id, name, food_type, image_url FROM local_food ORDER BY id')
    foods = cursor.fetchall()
    
    foods_needing_images = []
    for f in foods:
        print(f"{f['id']:2d}. {f['name']:30s} | {f['food_type']:15s} | {f['image_url'][:50] if f['image_url'] else 'MISSING'}")
        if not f['image_url'] or not f['image_url'].startswith('/static/images/'):
            foods_needing_images.append((f['id'], f['name']))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Artisans needing images: {len(artisans_needing_images)}/{len(artisans)}")
    if artisans_needing_images:
        print("  -", ", ".join([a[1] for a in artisans_needing_images]))
    
    print(f"Food items needing images: {len(foods_needing_images)}/{len(foods)}")
    if foods_needing_images:
        print("  -", ", ".join([f[1] for f in foods_needing_images]))
    
    conn.close()

if __name__ == '__main__':
    analyze()
