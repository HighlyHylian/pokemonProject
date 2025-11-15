import csv
import requests
import time

INPUT_FILE = "pokemon_list.txt"   # one Pokémon per line
OUTPUT_FILE = "pokemon_types.csv"

def get_pokemon_type(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    r = requests.get(url)

    if r.status_code != 200:
        print(f"[!] Could not find: {name}")
        return None, None

    data = r.json()
    types = [t["type"]["name"] for t in data["types"]]

    # Guarantee two columns
    type1 = types[0] if len(types) > 0 else ""
    type2 = types[1] if len(types) > 1 else ""

    return type1, type2

def main():
    with open(INPUT_FILE, "r") as f:
        pokemon = [line.strip() for line in f if line.strip()]

    with open(OUTPUT_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "type1", "type2"])

        for name in pokemon:
            print(f"Fetching {name}...")
            type1, type2 = get_pokemon_type(name)
            writer.writerow([name, type1, type2])
            time.sleep(0.3)  # avoid rate limits

    print(f"\nDone! CSV saved as: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
