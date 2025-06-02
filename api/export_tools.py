import csv
import json

def export_to_csv(data, filename="wifi_export.csv"):
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def export_to_json(data, filename="wifi_export.json"):
    with open(filename, "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, indent=4, ensure_ascii=False)

# Ejemplo de uso
if __name__ == "__main__":
    example_data = [
        {"city": "New York", "ssid": "LinkNYC Free Wi-Fi", "lat": 40.7128, "lon": -74.0060, "coverage": "High"},
        {"city": "Buenos Aires", "ssid": "BA WiFi", "lat": -34.6037, "lon": -58.3816, "coverage": "Medium"}
    ]
    export_to_csv(example_data)
    export_to_json(example_data)