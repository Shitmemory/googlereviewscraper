import requests
import csv
import time

API_KEY = ''  # Replace with your real Google Places API key
LOCATION = '28.6139,77.2090'  # Example: New Delhi
RADIUS = 10000  # in meters
TYPE = 'real_estate_agency'
OUTPUT_CSV = 'real_estate_leads.csv'

def fetch_places():
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={LOCATION}&radius={RADIUS}&type={TYPE}&key={API_KEY}"
    places = []

    while url:
        response = requests.get(url)
        data = response.json()

        for place in data.get('results', []):
            rating = place.get('rating', 0)
            total_reviews = place.get('user_ratings_total', 0)

            if rating <= 3.0:
             places.append({
                    'name': place.get('name'),
                    'rating': rating,
                    'reviews': total_reviews,
                    'address': place.get('vicinity'),
                    'place_id': place.get('place_id'),
                })

        next_page_token = data.get('next_page_token')
        if next_page_token:
            time.sleep(2)  # Required wait time for token activation
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={API_KEY}"
        else:
            break

    return places

def save_to_csv(places):
    if not places:
        print("No places found.")
        return

    with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=places[0].keys())
        writer.writeheader()
        writer.writerows(places)

    print(f"Saved {len(places)} agencies to {OUTPUT_CSV}")

# Run the script
if __name__ == "__main__":
    results = fetch_places()
    save_to_csv(results)