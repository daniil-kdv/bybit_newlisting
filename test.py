import json

# Load the JSON data
file_path = '/home/rook1e/project/bybit/kirby/new_listing.json'

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Function to remove "2024년 " from date strings
def remove_year_from_date(entry):
    entry['date'] = entry['date'].replace("2024년", "").strip()
    return entry

# Apply the function to all entries
updated_data = [remove_year_from_date(entry) for entry in data]

# Define the directory and file path for the updated JSON data
updated_file_path = '/home/rook1e/project/bybit/kirby/new_listing_updated.json'

# Save the updated JSON data
with open(updated_file_path, 'w', encoding='utf-8') as file:
    json.dump(updated_data, file, ensure_ascii=False, indent=4)

print("Updated JSON data saved to:", updated_file_path)

