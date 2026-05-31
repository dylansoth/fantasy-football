import json
import random

# Core Skill: Data Serialization (JSON)
# Developers use JSON (JavaScript Object Notation) to pass data between different
# languages (like Python and JavaScript) and systems (like a backend server and frontend).

def generate_mock_stats():
    """
    Generates a list of NFL Punters and their stats for a given week.
    This simulates the data structure we would get from a sports API.
    """
    punters = [
        {"name": "Ryan Stonehouse", "team": "TEN"},
        {"name": "A.J. Cole", "team": "LV"},
        {"name": "Mitch Wishnowsky", "team": "SF"},
        {"name": "Tress Way", "team": "WAS"},
        {"name": "Johnny Hekker", "team": "CAR"},
        {"name": "Bryan Anger", "team": "DAL"},
        {"name": "Logan Cooke", "team": "JAX"},
        {"name": "Corey Bojorquez", "team": "CLE"},
    ]

    raw_data = []
    
    for p in punters:
        # Generate semi-realistic stats for a single week of punting
        punts = random.randint(3, 8)
        avg_yards = random.uniform(43.0, 52.0)
        punt_yards = int(punts * avg_yards)
        
        # Touchbacks must be less than or equal to total punts
        touchbacks = random.randint(0, min(2, punts))
        
        # Punts inside 20 must be less than or equal to (total punts - touchbacks)
        inside_20 = random.randint(0, punts - touchbacks)
        
        # Punts inside 10 must be less than or equal to inside 20
        inside_10 = random.randint(0, inside_20)
        
        # Blocked punts are rare (0 in most games)
        blocked = 1 if random.random() < 0.05 else 0

        player_week_stats = {
            "name": p["name"],
            "team": p["team"],
            "punts": punts,
            "punt_yards": punt_yards,
            "inside_20": inside_20,
            "inside_10": inside_10,
            "touchbacks": touchbacks,
            "blocked": blocked
        }
        
        raw_data.append(player_week_stats)
        
    return raw_data

def main():
    print("Generating mock punting stats...")
    stats = generate_mock_stats()
    
    # Save the data to a local JSON file
    # This represents the intermediate cache file created by your data scraper
    output_filename = "raw_stats.json"
    with open(output_filename, "w") as f:
        json.dump(stats, f, indent=4)
        
    print(f"Success! Mock data saved to {output_filename}")
    print(f"Sample data generated: {stats[0]}")

if __name__ == "__main__":
    main()
