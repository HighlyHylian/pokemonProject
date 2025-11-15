import os
import csv
import requests
from PIL import Image, UnidentifiedImageError

CSV_FILE = 'pokemon_data.csv'
IMG_DIR = 'pokemon_images'

# keys for filenames
SPRITE_KEYS = ['front_default', 'front_shiny', 'back_default', 'back_shiny', 'official_artwork']

def fix_placeholders():
    with open(CSV_FILE) as f:
        rows = list(csv.DictReader(f))

    total_fixed = 0

    for row in rows:
        poke_id = row['id']
        for key in SPRITE_KEYS:
            url = row.get(key)
            if not url:
                continue

            filename = f"{poke_id}_{key}.png"
            filepath = os.path.join(IMG_DIR, filename)

            # skip files that exist
            if os.path.exists(filepath):
                try:
                    img = Image.open(filepath)
                    img.verify()
                    continue
                except (UnidentifiedImageError, IOError):
                    print(f"Found placeholder/corrupted image: {filename}")
            
            # try to redownload
            try:
                print(f"Downloading {filename}...")
                resp = requests.get(url, timeout=5)
                resp.raise_for_status()
                with open(filepath, 'wb') as f:
                    f.write(resp.content)

                # verify image
                img = Image.open(filepath)
                img.convert('RGB')  # Will fail if not valid
                print(f"Fixed {filename}")
                total_fixed += 1

            except Exception as e:
                print(f"Failed to fix {filename}: {e}")

    print(f"\nDone! Fixed {total_fixed} images.")

if __name__ == "__main__":
    os.makedirs(IMG_DIR, exist_ok=True)
    fix_placeholders()