import json
import csv
import datetime
from collections import defaultdict

# Load the ODI match data
def load_match_data():
    with open("odi_matches.json", "r", encoding="utf-8") as file:
        return json.load(file)

def calculate_toss_stats(matches):
    toss_stats = defaultdict(lambda: {"toss_wins": 0, "bat_first_wins": 0, "field_first_wins": 0})
    match_dates = []
    
    for match in matches:
        info = match.get("info", {})
        date = info.get("dates", [None])[0]
        if date:
            match_dates.append(date)
        
        toss = info.get("toss", {})
        winner = toss.get("winner")
        decision = toss.get("decision")
        outcome = info.get("outcome", {}).get("winner")
        
        if winner:
            toss_stats[winner]["toss_wins"] += 1
            if decision == "bat" and outcome == winner:
                toss_stats[winner]["bat_first_wins"] += 1
            elif decision == "field" and outcome == winner:
                toss_stats[winner]["field_first_wins"] += 1
    
    match_dates.sort()
    date_range = f"{match_dates[0]} to {match_dates[-1]}" if match_dates else "Unknown"
    
    return toss_stats, date_range

def save_toss_stats(toss_stats, date_range):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"toss_analysis_{timestamp}.csv"
    
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Team", "Toss Wins", "Bat First Wins", "Field First Wins", "Date Range"])
        
        for team, stats in toss_stats.items():
            writer.writerow([team, stats['toss_wins'], stats['bat_first_wins'], stats['field_first_wins'], date_range])
    
    print(f"Toss analysis saved to {output_file}")

def display_toss_stats(toss_stats, date_range):
    print("\nTOSS ANALYSIS IN ODIs")
    print(f"Data Range: {date_range}")
    
    for team, stats in toss_stats.items():
        print(f"\n{team}")
        print(f"Toss Wins: {stats['toss_wins']}")
        print(f"Wins After Batting First: {stats['bat_first_wins']}")
        print(f"Wins After Fielding First: {stats['field_first_wins']}")

if __name__ == "__main__":
    matches = load_match_data()
    toss_stats, date_range = calculate_toss_stats(matches)
    display_toss_stats(toss_stats, date_range)
    save_toss_stats(toss_stats, date_range)

