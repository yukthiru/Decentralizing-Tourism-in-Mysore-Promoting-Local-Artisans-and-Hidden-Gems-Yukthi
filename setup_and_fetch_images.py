#!/usr/bin/env python
"""
Master setup script: Seeds database and fetches all images from Google.
Run this once to get the full application ready.
"""

import sys
import subprocess

def run_command(cmd, description):
    """Run a command and report status."""
    print(f'\n{"="*60}')
    print(f'{description}')
    print(f'{"="*60}')
    try:
        result = subprocess.run(cmd, check=True, shell=True)
        print(f'\n✓ {description} - SUCCESS')
        return True
    except subprocess.CalledProcessError as e:
        print(f'\n✗ {description} - FAILED')
        return False

def main():
    """Run the setup sequence."""
    print('\n' + '='*60)
    print('MYSORE UNSEEN - COMPLETE SETUP')
    print('='*60)
    
    # Step 1: Seed the database
    if not run_command(
        'python seed_data.py',
        'Step 1: Seeding Database'
    ):
        print('Database seeding failed. Stopping.')
        sys.exit(1)
    
    # Step 2: Fetch images for artisans
    if not run_command(
        'python fetch_images_comprehensive.py --target artisans',
        'Step 2: Fetching Artisan Images'
    ):
        print('Warning: Artisan image fetching had issues, but continuing...')
    
    # Step 3: Fetch images for food
    if not run_command(
        'python fetch_images_comprehensive.py --target food',
        'Step 3: Fetching Food Discovery Images'
    ):
        print('Warning: Food image fetching had issues, but continuing...')
    
    # Step 4: Fetch images for products
    if not run_command(
        'python fetch_images_comprehensive.py --target products',
        'Step 4: Fetching Artisan Product Images'
    ):
        print('Warning: Product image fetching had issues, but continuing...')
    
    # Step 5: Fetch images for hidden gems
    if not run_command(
        'python fetch_images_comprehensive.py --target gems',
        'Step 5: Fetching Hidden Gems Images'
    ):
        print('Warning: Gem image fetching had issues, but continuing...')
    
    # Step 6: Fetch images for market stalls
    if not run_command(
        'python fetch_images_comprehensive.py --target stalls',
        'Step 6: Fetching Market Stall Images'
    ):
        print('Warning: Stall image fetching had issues, but continuing...')
    
    print('\n' + '='*60)
    print('✓ SETUP COMPLETE!')
    print('='*60)
    print('\nYour application is ready. Start it with:')
    print('  python app.py')
    print('\nThen open: http://localhost:5000')
    print('='*60 + '\n')

if __name__ == '__main__':
    main()
