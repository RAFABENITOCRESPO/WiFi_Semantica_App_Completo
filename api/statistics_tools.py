def calculate_stats(data):
    from collections import Counter
    city_counts = Counter([item["city"] for item in data])
    coverage_levels = Counter([item["coverage"] for item in data])
    return {
        "total_points": len(data),
        "points_per_city": dict(city_counts),
        "coverage_distribution": dict(coverage_levels)
    }

# Ejemplo de uso
if __name__ == "__main__":
    sample_data = [
        {"city": "New York", "coverage": "High"},
        {"city": "New York", "coverage": "High"},
        {"city": "Buenos Aires", "coverage": "Medium"},
        {"city": "Buenos Aires", "coverage": "Low"},
    ]
    print(calculate_stats(sample_data))