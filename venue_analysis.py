import json
import csv
import datetime
from collections import defaultdict

# Load the ODI match data
def load_match_data():
    with open("odi_matches.json", "r", encoding="utf-8") as file:
        return json.load(file)

def calculate_venue_stats(matches):
    venue_stats = defaultdict(lambda: {"matches": 0, "highest_score": 0, "lowest_score": float('inf'), "neutral_wins": 0})
    match_dates = []
    
    for match in matches:
        info = match.get("info", {})
        date = info.get("dates", [None])[0]
        if date:
            match_dates.append(date)
        
        venue = info.get("venue", "Unknown Venue")
        venue_stats[venue]["matches"] += 1
        
        teams = info.get("teams", [])
        outcome = info.get("outcome", {}).get("winner")
        
        innings = match.get("innings", [])
        team_scores = {}
        
        for inning in innings:
            for inning_key, entry in inning.items():
                if isinstance(entry, dict):  # Ensure entry is a dictionary
                    team = entry.get("team", "Unknown Team")
                    
                    # Handle 'runs' key correctly
                    total_score = entry.get("runs", 0)
                    if isinstance(total_score, dict):  
                        total_score = total_score.get("total", 0)

                    for delivery in entry.get("deliveries", []):
                        for _, delivery_data in delivery.items():
                            delivery_runs = delivery_data.get("runs", 0)
                            if isinstance(delivery_runs, dict):
                                total_score += delivery_runs.get("total", 0)
                    
                    team_scores[team] = max(team_scores.get(team, 0), total_score)
        
        if team_scores:
            max_score = max(team_scores.values())
            min_score = min(team_scores.values())
            
            venue_stats[venue]["highest_score"] = max(venue_stats[venue]["highest_score"], max_score)
            venue_stats[venue]["lowest_score"] = min(venue_stats[venue]["lowest_score"], min_score)
        
        if outcome and outcome not in teams:  # Win at a neutral venue
            venue_stats[venue]["neutral_wins"] += 1
    
    match_dates.sort()
    date_range = f"{match_dates[0]} to {match_dates[-1]}" if match_dates else "Unknown"
    
    return venue_stats, date_range

def save_venue_stats(venue_stats, date_range):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"venue_analysis_{timestamp}.csv"
    
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Venue", "Matches Played", "Highest Score", "Lowest Score", "Neutral Wins", "Date Range"])
        
        for venue, stats in venue_stats.items():
            lowest_score = stats['lowest_score'] if stats['lowest_score'] != float('inf') else 0
            writer.writerow([venue, stats['matches'], stats['highest_score'], lowest_score, stats['neutral_wins'], date_range])
    
    print(f"Venue analysis saved to {output_file}")

def display_venue_stats(venue_stats, date_range):
    print("\nVENUE ANALYSIS IN ODIs")
    print(f"Data Range: {date_range}")
    
    for venue, stats in venue_stats.items():
        lowest_score = stats['lowest_score'] if stats['lowest_score'] != float('inf') else 0
        print(f"\n{venue}")
        print(f"Matches Played: {stats['matches']}")
        print(f"Highest Score: {stats['highest_score']}")
        print(f"Lowest Score: {lowest_score}")
        print(f"Neutral Wins: {stats['neutral_wins']}")

if __name__ == "__main__":
    matches = load_match_data()
    venue_stats, date_range = calculate_venue_stats(matches)
    display_venue_stats(venue_stats, date_range)
    save_venue_stats(venue_stats, date_range)

