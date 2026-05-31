import json

# Core Skill: Data Processing & Business Logic separation
# Good software architecture keeps the "data ingestion" (getting the stats)
# separate from the "business logic" (calculating the custom scores).

def calculate_custom_punter_score(stats):
    """
    Applies our custom 2026 Punter Scoring Rules:
    - Yards: +0.04 pts per yard (1 point per 25 yards)
    - Inside 20 (but NOT inside 10): +1.5 pts
    - Inside 10: +3.0 pts
    - Touchbacks: -1.0 pt
    - Blocked Punts: -3.0 pts
    """
    score = 0.0
    
    # 1. Yards scoring
    score += stats.get("punt_yards", 0) * 0.04
    
    # 2. Inside the 20 & 10 scoring
    # Note: Punts inside 10 are technically inside 20.
    # We subtract inside_10 from inside_20 to get punts that landed strictly between the 10 and 20.
    i20_only = stats.get("inside_20", 0) - stats.get("inside_10", 0)
    score += i20_only * 1.5
    score += stats.get("inside_10", 0) * 3.0
    
    # 3. Penalties
    score -= stats.get("touchbacks", 0) * 1.0
    score -= stats.get("blocked", 0) * 3.0
    
    # Round to 2 decimal places (standard for fantasy football)
    return round(score, 2)

def main():
    print("Reading raw_stats.json...")
    
    try:
        with open("raw_stats.json", "r") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print("Error: raw_stats.json not found! Please run generate_mock_data.py first.")
        return

    processed_scores = []
    
    for player in raw_data:
        score = calculate_custom_punter_score(player)
        
        # Construct the processed player record for the website
        processed_player = {
            "name": player["name"],
            "team": player["team"],
            "punts": player["punts"],
            "punt_yards": player["punt_yards"],
            "inside_20": player["inside_20"],
            "inside_10": player["inside_10"],
            "touchbacks": player["touchbacks"],
            "blocked": player["blocked"],
            "fantasy_score": score
        }
        processed_scores.append(processed_player)
        
    # Core Skill: Sorting Data
    # Sort players by fantasy_score in descending order (highest score first)
    # lambda is a small anonymous function in Python. It tells sorted() to look at 'fantasy_score'
    processed_scores = sorted(processed_scores, key=lambda x: x["fantasy_score"], reverse=True)

    # Save the output to a new file that the frontend will load
    output_filename = "punter_scores.json"
    with open(output_filename, "w") as f:
        json.dump(processed_scores, f, indent=4)
        
    print(f"Success! Processed fantasy scores saved to {output_filename}")
    print("\nLeaderboard for the week:")
    for rank, player in enumerate(processed_scores, 1):
        print(f"{rank}. {player['name']} ({player['team']}): {player['fantasy_score']} pts")

if __name__ == "__main__":
    main()
