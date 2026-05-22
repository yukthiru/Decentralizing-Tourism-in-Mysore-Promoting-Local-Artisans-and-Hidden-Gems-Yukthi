#!/usr/bin/env python
"""
Execute setup and image fetching sequence.
"""
import os
import sys

# Change to the project directory
os.chdir(r'c:\Users\Yukthi R U\Downloads\inunity antigravity\mysore-unseen')
sys.path.insert(0, os.getcwd())

print("Step 1: Importing and running seed_data...")
try:
    from seed_data import seed_data
    seed_data()
    print("✓ Database seeded successfully!")
except Exception as e:
    print(f"✗ Error seeding database: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 2: Fetching images for artisans, food, and products...")
try:
    from fetch_images_comprehensive import (
        fetch_artisan_images,
        fetch_food_images,
        fetch_artisan_product_images,
        fetch_hidden_gem_images,
        fetch_market_stall_images
    )
    
    print("\n--- Fetching Artisan Images ---")
    fetch_artisan_images()
    
    print("\n--- Fetching Food Discovery Images ---")
    fetch_food_images()
    
    print("\n--- Fetching Artisan Product Images ---")
    fetch_artisan_product_images()
    
    print("\n--- Fetching Hidden Gem Images ---")
    fetch_hidden_gem_images()
    
    print("\n--- Fetching Market Stall Images ---")
    fetch_market_stall_images()
    
    print("\n✓ All images fetched successfully!")
except Exception as e:
    print(f"✗ Error fetching images: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("✓ SETUP COMPLETE!")
print("="*60)
print("\nYour application is ready to use:")
print("  - Database: mysore_unseen.db")
print("  - Images: static/images/")
print("\nStart the app with: python app.py")
print("Then open: http://localhost:5000")
print("="*60 + "\n")
