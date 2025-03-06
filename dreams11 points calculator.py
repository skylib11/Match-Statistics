import json
import pandas as pd
from collections import defaultdict
from datetime import datetime

# Define the 8 teams to filter matches
VALID_TEAMS = {"India", "New Zealand", "Bangladesh", "Pakistan", "South Africa", "England", "Australia"}

# Load ODI match data and filter matches since January 2024
def load_valid_matches(file_path):
    with open(file_path, 'r') as f:
        matches = json.load(f)
    if isinstance(matches, dict):
        matches = list(matches.values())
    
    def extract_date(match):
        date_str = match.get("info", {}).get("dates", ["0000-00-00"])[0]
        return datetime.strptime(date_str, "%Y-%m-%d")
    
    matches = sorted(matches, key=extract_date, reverse=True)  # Sort by date (latest first)
    
    valid_matches = []
    for match in matches:
        match_info = match.get("info", {})
        match_date = extract_date(match)
        teams = set(match_info.get("teams", []))
        
        print(f"Checking Match: {teams} on {match_date}")  # Debugging
        
        # Allow matches where at least one team is in VALID_TEAMS
        if match_date >= datetime(2024, 1, 1) and teams & VALID_TEAMS:
            valid_matches.append(match)
    
    return valid_matches

# Calculate fantasy points for a player
def calculate_fantasy_points(player_name, match_data):
    points = 0
    runs = 0
    boundaries = 0
    sixes = 0
    wickets = 0
    catches = 0
    run_outs = 0
    dot_balls = 0
    
    for inning in match_data.get("innings", []):
        for over in inning.get("overs", []):
            for delivery in over.get("deliveries", []):
                if delivery.get("batter") == player_name:
                    runs += delivery["runs"].get("batter", 0)
                    if delivery["runs"].get("batter", 0) == 4:
                        boundaries += 1
                    if delivery["runs"].get("batter", 0) == 6:
                        sixes += 1
                
                if delivery.get("bowler") == player_name:
                    if "wickets" in delivery:
                        wickets += len(delivery["wickets"])
                        for w in delivery["wickets"]:
                            if w.get("kind") in ["bowled", "lbw"]:
                                points += 8  # Bonus for LBW/Bowled
                        if delivery["runs"].get("total", 0) == 0:
                            dot_balls += 1
                
                if "wickets" in delivery:
                    for w in delivery["wickets"]:
                        if w.get("kind") == "caught" and player_name in [f["name"] for f in w.get("fielders", [])]:
                            catches += 1
                        elif w.get("kind") == "run out" and player_name in [f["name"] for f in w.get("fielders", [])]:
                            run_outs += 1
    
    # Apply Dream11 scoring system
    points += runs
    points += boundaries * 4
    points += sixes * 6
    if runs >= 25: points += 4
    if runs >= 50: points += 8
    if runs >= 75: points += 12
    if runs >= 100: points += 16
    if runs >= 125: points += 20
    if runs >= 150: points += 24
    if runs == 0 and (boundaries > 0 or sixes > 0): points -= 3
    points += wickets * 25
    if wickets >= 4: points += 4
    if wickets >= 5: points += 8
    points += catches * 8
    if catches >= 3: points += 4
    points += run_outs * 12
    points += (dot_balls // 3)
    
    return points

# Process all valid matches and save results
def process_matches(matches_file, output_file):
    valid_matches = load_valid_matches(matches_file)
    all_data = []
    
    for match in valid_matches:
        match_info = match.get("info", {})
        team1, team2 = match_info.get("teams", ["Unknown", "Unknown"])
        match_date = match_info.get("dates", ["Unknown"])[0]
        
        print(f"\n📢 Processing Match: {team1} vs {team2} on {match_date}")
        
        players = set()
        for inning in match.get("innings", []):
            for over in inning.get("overs", []):
                for delivery in over.get("deliveries", []):
                    if "batter" in delivery:
                        players.add(delivery["batter"])
                    if "bowler" in delivery:
                        players.add(delivery["bowler"])
                    for w in delivery.get("wickets", []):
                        if "fielders" in w:
                            players.update([f["name"] for f in w["fielders"]])
        
        for player in players:
            points = calculate_fantasy_points(player, match)
            all_data.append([match_date, team1, team2, player, points])
    
    df = pd.DataFrame(all_data, columns=["Match Date", "Team 1", "Team 2", "Player", "Fantasy Points"])
    df.to_csv(output_file, index=False)
    print(f"✅ Fantasy points saved to {output_file}")

# File paths
matches_file = "odi_matches.json"
output_file = "fantasy_points_2024.csv"

# Process and save fantasy points
process_matches(matches_file, output_file)

