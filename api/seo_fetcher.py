import random

def fetch_seo_data(keyword: str) -> list:
    """
    Generate mock SEO data in the same format as the API (TODO) for a given keyword.
    Returns a list with a single dictionary containing SEO metrics and a history trend.
    """
    # Generate mock values
    volume = random.randint(10, 10000)
    cpc = round(random.uniform(0.0, 5.0), 2)
    difficulty = random.randint(10, 100)
    
    mock_data = [{
        "is_data_found": True,
        "keyword": keyword,
        "volume": volume,
        "cpc": cpc,
        "difficulty": difficulty
    }]
    
    return mock_data

# Example usage
if __name__ == "__main__":
    keyword = "seranking.com"
    data = fetch_seo_data(keyword)
    import json
    print(json.dumps(data, indent=2))
